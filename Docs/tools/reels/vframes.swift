// vframes: раскадровка видео (клипы Higgsfield) в JPEG для studio.py, без ffmpeg.
// Кадр вписывается в WxH с обрезкой краев (как «заполнить»).
// Сборка: DEVELOPER_DIR=~/Downloads/Xcode.app/Contents/Developer xcrun swiftc -O vframes.swift -o vframes
// Запуск: vframes in.mp4 outdir fps width height
import AVFoundation
import CoreGraphics
import ImageIO

let a = CommandLine.arguments
guard a.count == 6, let fps = Double(a[3]), let W = Int(a[4]), let H = Int(a[5]) else {
    FileHandle.standardError.write("usage: vframes in.mp4 outdir fps width height\n".data(using: .utf8)!); exit(2)
}
let asset = AVURLAsset(url: URL(fileURLWithPath: a[1]))
let gen = AVAssetImageGenerator(asset: asset)
gen.appliesPreferredTrackTransform = true
gen.requestedTimeToleranceBefore = .zero
gen.requestedTimeToleranceAfter = .zero
let dur = CMTimeGetSeconds(asset.duration)
var i = 0
while Double(i) / fps < dur {
    let t = CMTime(seconds: Double(i) / fps, preferredTimescale: 600)
    if let cg = try? gen.copyCGImage(at: t, actualTime: nil),
       let ctx = CGContext(data: nil, width: W, height: H, bitsPerComponent: 8, bytesPerRow: 0,
                           space: CGColorSpaceCreateDeviceRGB(), bitmapInfo: CGImageAlphaInfo.noneSkipLast.rawValue) {
        let sw = Double(cg.width), sh = Double(cg.height), k = max(Double(W) / sw, Double(H) / sh)
        ctx.interpolationQuality = .high
        ctx.draw(cg, in: CGRect(x: (Double(W) - sw * k) / 2, y: (Double(H) - sh * k) / 2, width: sw * k, height: sh * k))
        if let img = ctx.makeImage(),
           let dest = CGImageDestinationCreateWithURL(URL(fileURLWithPath: String(format: "%@/f%05d.jpg", a[2], i)) as CFURL,
                                                      "public.jpeg" as CFString, 1, nil) {
            CGImageDestinationAddImage(dest, img, [kCGImageDestinationLossyCompressionQuality: 0.92] as CFDictionary)
            CGImageDestinationFinalize(dest)
        }
    }
    i += 1
}
print(i)
