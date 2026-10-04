// mux: видео (H.264 из mp4enc) + звук (AAC .m4a) → mp4 без перекодирования.
// Сборка: DEVELOPER_DIR=~/Downloads/Xcode.app/Contents/Developer xcrun swiftc -O mux.swift -o mux
import AVFoundation

let args = CommandLine.arguments
guard args.count == 4 else {
    FileHandle.standardError.write("usage: mux video.mp4 audio.m4a out.mp4\n".data(using: .utf8)!); exit(2)
}
let video = AVURLAsset(url: URL(fileURLWithPath: args[1]))
let audio = AVURLAsset(url: URL(fileURLWithPath: args[2]))
let outURL = URL(fileURLWithPath: args[3])
try? FileManager.default.removeItem(at: outURL)

let comp = AVMutableComposition()
let dur = video.duration
guard let vt = video.tracks(withMediaType: .video).first,
      let cv = comp.addMutableTrack(withMediaType: .video, preferredTrackID: kCMPersistentTrackID_Invalid) else { exit(3) }
try cv.insertTimeRange(CMTimeRange(start: .zero, duration: dur), of: vt, at: .zero)
cv.preferredTransform = vt.preferredTransform
if let at = audio.tracks(withMediaType: .audio).first,
   let ca = comp.addMutableTrack(withMediaType: .audio, preferredTrackID: kCMPersistentTrackID_Invalid) {
    try ca.insertTimeRange(CMTimeRange(start: .zero, duration: CMTimeMinimum(dur, audio.duration)), of: at, at: .zero)
}
guard let ex = AVAssetExportSession(asset: comp, presetName: AVAssetExportPresetPassthrough) else { exit(4) }
ex.outputURL = outURL
ex.outputFileType = .mp4
let sem = DispatchSemaphore(value: 0)
ex.exportAsynchronously { sem.signal() }
sem.wait()
if ex.status != .completed {
    FileHandle.standardError.write("mux failed: \(String(describing: ex.error))\n".data(using: .utf8)!); exit(5)
}
