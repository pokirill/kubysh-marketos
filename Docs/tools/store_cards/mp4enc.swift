// Кодировщик H.264 без ffmpeg: читает сырые кадры BGRA из stdin и пишет MP4 через AVFoundation.
// Сборка: xcrun swiftc -O mp4enc.swift -o mp4enc
// Запуск: mp4enc out.mp4 1080 1350 30 < frames.raw
import AVFoundation
import Foundation

let args = CommandLine.arguments
guard args.count == 5, let w = Int(args[2]), let h = Int(args[3]), let fps = Int32(args[4]) else {
    FileHandle.standardError.write("usage: mp4enc out.mp4 width height fps\n".data(using: .utf8)!)
    exit(2)
}
let out = URL(fileURLWithPath: args[1])
try? FileManager.default.removeItem(at: out)
let writer = try AVAssetWriter(outputURL: out, fileType: .mp4)
let input = AVAssetWriterInput(mediaType: .video, outputSettings: [
    AVVideoCodecKey: AVVideoCodecType.h264,
    AVVideoWidthKey: w,
    AVVideoHeightKey: h,
    AVVideoColorPropertiesKey: [
        AVVideoColorPrimariesKey: AVVideoColorPrimaries_ITU_R_709_2,
        AVVideoTransferFunctionKey: AVVideoTransferFunction_ITU_R_709_2,
        AVVideoYCbCrMatrixKey: AVVideoYCbCrMatrix_ITU_R_709_2,
    ],
    AVVideoCompressionPropertiesKey: [
        AVVideoAverageBitRateKey: 12_000_000,
        AVVideoProfileLevelKey: AVVideoProfileLevelH264HighAutoLevel,
        AVVideoMaxKeyFrameIntervalKey: Int(fps) * 2,
        AVVideoExpectedSourceFrameRateKey: Int(fps),
    ],
])
input.expectsMediaDataInRealTime = false
let adaptor = AVAssetWriterInputPixelBufferAdaptor(assetWriterInput: input, sourcePixelBufferAttributes: [
    kCVPixelBufferPixelFormatTypeKey as String: kCVPixelFormatType_32BGRA,
    kCVPixelBufferWidthKey as String: w,
    kCVPixelBufferHeightKey as String: h,
])
writer.add(input)
guard writer.startWriting() else { fatalError("startWriting: \(String(describing: writer.error))") }
writer.startSession(atSourceTime: .zero)

let frameBytes = w * h * 4
let stdin = FileHandle.standardInput
var index: Int64 = 0
while true {
    var data = Data(capacity: frameBytes)
    while data.count < frameBytes {
        let chunk = stdin.readData(ofLength: frameBytes - data.count)
        if chunk.isEmpty { break }
        data.append(chunk)
    }
    if data.count < frameBytes { break }
    while !input.isReadyForMoreMediaData { usleep(2000) }
    var buffer: CVPixelBuffer?
    CVPixelBufferPoolCreatePixelBuffer(nil, adaptor.pixelBufferPool!, &buffer)
    guard let pb = buffer else { fatalError("no pixel buffer") }
    CVPixelBufferLockBaseAddress(pb, [])
    let base = CVPixelBufferGetBaseAddress(pb)!
    let rowBytes = CVPixelBufferGetBytesPerRow(pb)
    data.withUnsafeBytes { raw in
        for y in 0..<h { memcpy(base + y * rowBytes, raw.baseAddress! + y * w * 4, w * 4) }
    }
    CVPixelBufferUnlockBaseAddress(pb, [])
    adaptor.append(pb, withPresentationTime: CMTime(value: index, timescale: fps))
    index += 1
}
input.markAsFinished()
let done = DispatchSemaphore(value: 0)
writer.finishWriting { done.signal() }
done.wait()
print("mp4enc: \(index) frames, status \(writer.status.rawValue)\(writer.error.map { " " + $0.localizedDescription } ?? "")")
