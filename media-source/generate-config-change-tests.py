#!/usr/bin/python
# Copyright (C) 2013 Google Inc. All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

"""
This is a script that generates the content and HTML files for Media Source
codec config change LayoutTests.
"""
import json
import os

DURATION = 2
MEDIA_FORMATS = ['webm', 'mp4']
ENCODE_SETTINGS = [
    ## Video-only files
    # Frame rate changes
    {'fs': '320x240', 'fr': 24, 'kfr': 8, 'c': '#ff0000', 'vbr': 128, 'abr': 0, 'asr': 0, 'ach': 0, 'afreq': 0},
    {'fs': '320x240', 'fr': 30, 'kfr': 10, 'c': '#ff0000', 'vbr': 128, 'abr': 0, 'asr': 0, 'ach': 0, 'afreq': 0},
    # Frame size change
    {'fs': '640x480', 'fr': 30, 'kfr': 10, 'c': '#00ff00', 'vbr': 128, 'abr': 0, 'asr': 0, 'ach': 0, 'afreq': 0},
    # Bitrate change
    {'fs': '320x240', 'fr': 30, 'kfr': 10, 'c': '#ff00ff', 'vbr': 256, 'abr': 0, 'asr': 0, 'ach': 0, 'afreq': 0},

    ## Audio-only files
    # Bitrate/Codebook changes
    {'fs': '0x0', 'fr': 0, 'kfr': 0, 'c': '#000000', 'vbr': 0, 'abr': 128, 'asr': 44100, 'ach': 1, 'afreq': 2000},
    {'fs': '0x0', 'fr': 0, 'kfr': 0, 'c': '#000000', 'vbr': 0, 'abr': 192, 'asr': 44100, 'ach': 1, 'afreq': 4000},

    ## Audio-Video files
    # Frame size change.
    {'fs': '320x240', 'fr': 30, 'kfr': 10, 'c': '#ff0000', 'vbr': 256, 'abr': 128, 'asr': 44100, 'ach': 1, 'afreq': 2000},
    {'fs': '640x480', 'fr': 30, 'kfr': 10, 'c': '#00ff00', 'vbr': 256, 'abr': 128, 'asr': 44100, 'ach': 1, 'afreq': 2000},
    # Audio bitrate change.
    {'fs': '640x480', 'fr': 30, 'kfr': 10, 'c': '#00ff00', 'vbr': 256, 'abr': 192, 'asr': 44100, 'ach': 1, 'afreq': 4000},
    # Video bitrate change.
    {'fs': '640x480', 'fr': 30, 'kfr': 10, 'c': '#00ffff', 'vbr': 512, 'abr': 128, 'asr': 44100, 'ach': 1, 'afreq': 2000},
]

CONFIG_CHANGE_TESTS = [
    ["v-framerate", 0, 1, "Tests %s video-only frame rate changes."],
    ["v-framesize", 1, 2, "Tests %s video-only frame size changes."],
    ["v-bitrate", 1, 3, "Tests %s video-only bitrate changes."],
    ["a-bitrate", 4, 5, "Tests %s audio-only bitrate changes."],
    ["av-framesize", 6, 7, "Tests %s frame size changes in multiplexed content."],
    ["av-audio-bitrate", 7, 8, "Tests %s audio bitrate changes in multiplexed content."],
    ["av-video-bitrate", 7, 9, "Tests %s video bitrate changes in multiplexed content."]
]

CODEC_INFO = {
    "mp4": {"audio": "mp4a.40.2", "video": "avc1.4D4001"},
    "webm": {"audio": "vorbis", "video": "vp8"}
}

HTML_TEMPLATE = """<!DOCTYPE html>
<html>
    <head>
        <script src="/w3c/resources/testharness.js"></script>
        <script src="/w3c/resources/testharnessreport.js"></script>
        <script src="mediasource-util.js"></script>
        <script src="mediasource-config-changes.js"></script>
    </head>
    <body>
        <div id="log"></div>
        <script>
            mediaSourceConfigChangeTest("%(media_format)s", "%(idA)s", "%(idB)s", "%(description)s");
        </script>
    </body>
</html>
"""

def run(cmd_line):
    os.system(" ".join(cmd_line))

def generate_manifest(filename, media_filename, media_format, has_audio, has_video):
    major_type = "video" if has_video else "audio"
    codecs = []
    if has_video:
        codecs.append(CODEC_INFO[media_format]["video"])

    if has_audio:
        codecs.append(CODEC_INFO[media_format]["audio"])

    mimetype = "%s/%s;codecs=\"%s\"" % (major_type, media_format, ",".join(codecs))

    manifest = { 'url': media_filename, 'type': mimetype}

    with open(filename, "wb") as f:
        f.write(json.dumps(manifest, indent=4, separators=(',', ': ')))

def generate_test_html(media_format, config_change_tests, encoding_ids):
    for test_info in config_change_tests:
        filename = f"../../media-source/mediasource-config-change-{media_format}-{test_info[0]}.html"
        html = HTML_TEMPLATE % {'media_format': media_format,
                                 'idA': encoding_ids[test_info[1]],
                                 'idB': encoding_ids[test_info[2]],
                                 'description':  test_info[3] % (media_format)}
        with open(filename, "wb") as f:
            f.write(html)


def main():
    encoding_ids = []

    for media_format in MEDIA_FORMATS:
        run(["mkdir ", media_format])

        for settings in ENCODE_SETTINGS:
            video_bitrate = settings['vbr']
            has_video = (video_bitrate > 0)

            audio_bitrate = settings['abr']
            has_audio = (audio_bitrate > 0)
            bitrate = video_bitrate + audio_bitrate

            frame_size = settings['fs']
            frame_rate = settings['fr']
            keyframe_rate = settings['kfr']
            color = settings['c']

            sample_rate = settings['asr']
            channels = settings['ach']
            frequency = settings['afreq']

            cmdline = ["ffmpeg", "-y"]

            id_prefix = ""
            id_params = ""
            if has_audio:
                id_prefix += "a"
                id_params += f"-{sample_rate}Hz-{channels}ch"

                channel_layout = "FC"
                sin_func = f"sin({frequency}*2*PI*t)"
                func = sin_func
                if channels == 2:
                    channel_layout += "|BC"
                    func += f"|{sin_func}"

                cmdline += ["-f", "lavfi", "-i", "aevalsrc=\"%s:s=%s:c=%s:d=%s\"" % (func, sample_rate, channel_layout, DURATION)]

            if has_video:
                id_prefix += "v"
                id_params += f"-{frame_size}-{frame_rate}fps-{keyframe_rate}kfr"

                cmdline += [
                    "-f",
                    "lavfi",
                    "-i",
                    f"color={color}:duration={DURATION}:size={frame_size}:rate={frame_rate}",
                ]

            if has_audio:
                cmdline += ["-b:a", f"{audio_bitrate}k"]

            if has_video:
                cmdline += ["-b:v", f"{video_bitrate}k"]
                cmdline += ["-keyint_min", f"{keyframe_rate}"]
                cmdline += ["-g", f"{keyframe_rate}"]


                textOverlayInfo = "'drawtext=fontfile=Mono:fontsize=32:text=Time\\\\:\\\\ %{pts}"
                textOverlayInfo += ",drawtext=fontfile=Mono:fontsize=32:y=32:text=Size\\\\:\\\\ %s" % (frame_size)
                textOverlayInfo += ",drawtext=fontfile=Mono:fontsize=32:y=64:text=Bitrate\\\\:\\\\ %s" % (bitrate)
                textOverlayInfo += ",drawtext=fontfile=Mono:fontsize=32:y=96:text=FrameRate\\\\:\\\\ %s" % (frame_rate)
                textOverlayInfo += ",drawtext=fontfile=Mono:fontsize=32:y=128:text=KeyFrameRate\\\\:\\\\ %s" % (keyframe_rate)

                if has_audio:
                    textOverlayInfo += ",drawtext=fontfile=Mono:fontsize=32:y=160:text=SampleRate\\\\:\\\\ %s" % (sample_rate)
                    textOverlayInfo += ",drawtext=fontfile=Mono:fontsize=32:y=192:text=Channels\\\\:\\\\ %s" % (channels)

                textOverlayInfo += "'"
                cmdline += ["-vf", textOverlayInfo]

            encoding_id = f"{id_prefix}-{bitrate}k{id_params}"

            if len(encoding_ids) < len(ENCODE_SETTINGS):
                encoding_ids.append(encoding_id)

            filename_base = f"{media_format}/test-{encoding_id}"
            media_filename = f"{filename_base}.{media_format}"
            manifest_filename = f"{filename_base}-manifest.json"

            cmdline.append(media_filename)
            run(cmdline)

            # Remux file so it conforms to MSE bytestream requirements.
            if media_format == "webm":
                tmp_filename = f"{media_filename}.tmp"
                run(["mse_webm_remuxer", media_filename, tmp_filename])
                run(["mv", tmp_filename, media_filename])
            elif media_format == "mp4":
                run(["MP4Box", "-dash", "250", "-rap", media_filename])
                run(["mv", f"{filename_base}_dash.mp4", media_filename])
                run(["rm", f"{filename_base}_dash.mpd"])

            generate_manifest(manifest_filename, media_filename, media_format, has_audio, has_video)
        generate_test_html(media_format, CONFIG_CHANGE_TESTS, encoding_ids)

if __name__ == '__main__':
    main()
