// Ускорение речи без смены высоты: tstretch in.wav out.wav 1.2 (AVAudioUnitTimePitch, офлайн).
import AVFoundation
let inURL = URL(fileURLWithPath: CommandLine.arguments[1]), outURL = URL(fileURLWithPath: CommandLine.arguments[2])
let rate = Float(CommandLine.arguments[3])!
let file = try! AVAudioFile(forReading: inURL)
let fmt = file.processingFormat
let engine = AVAudioEngine(), player = AVAudioPlayerNode(), tp = AVAudioUnitTimePitch()
tp.rate = rate
engine.attach(player); engine.attach(tp)
engine.connect(player, to: tp, format: fmt); engine.connect(tp, to: engine.mainMixerNode, format: fmt)
try! engine.enableManualRenderingMode(.offline, format: fmt, maximumFrameCount: 4096)
try! engine.start(); player.scheduleFile(file, at: nil); player.play()
var out: AVAudioFile? = try! AVAudioFile(forWriting: outURL, settings: file.fileFormat.settings)
let buf = AVAudioPCMBuffer(pcmFormat: engine.manualRenderingFormat, frameCapacity: 4096)!
let total = AVAudioFramePosition(Double(file.length) / Double(rate)) + 2048
while engine.manualRenderingSampleTime < total {
  let n = min(AVAudioFrameCount(4096), AVAudioFrameCount(total - engine.manualRenderingSampleTime))
  if try! engine.renderOffline(n, to: buf) == .success { try! out!.write(from: buf) } else { break }
}
engine.stop(); out = nil
