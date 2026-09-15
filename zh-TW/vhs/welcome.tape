# VHS documentation
#
# Output:
#   Output <path>.gif               Create a GIF output at the given <path>
#   Output <path>.mp4               Create an MP4 output at the given <path>
#   Output <path>.webm              Create a WebM output at the given <path>
#
# Require:
#   Require <string>                Ensure a program is on the $PATH to proceed
#
# Settings:
#   Set FontSize <number>           Set the font size of the terminal
#   Set FontFamily <string>         Set the font family of the terminal
#   Set Height <number>             Set the height of the terminal
#   Set Width <number>              Set the width of the terminal
#   Set LetterSpacing <float>       Set the font letter spacing (tracking)
#   Set LineHeight <float>          Set the font line height
#   Set LoopOffset <float>%         Set the starting frame offset for the GIF loop
#   Set Theme <json|string>         Set the theme of the terminal
#   Set Padding <number>            Set the padding of the terminal
#   Set Framerate <number>          Set the framerate of the recording
#   Set PlaybackSpeed <float>       Set the playback speed of the recording
#   Set MarginFill <file|#000000>   Set the file or color the margin will be filled with.
#   Set Margin <number>             Set the size of the margin. Has no effect if MarginFill isn't set.
#   Set BorderRadius <number>       Set terminal border radius, in pixels.
#   Set WindowBar <string>          Set window bar type. (one of: Rings, RingsRight, Colorful, ColorfulRight)
#   Set WindowBarSize <number>      Set window bar size, in pixels. Default is 40.
#   Set TypingSpeed <time>          Set the typing speed of the terminal. Default is 50ms.
#
# Sleep:
#   Sleep <time>                    Sleep for a set amount of <time> in seconds
#
# Type:
#   Type[@<time>] "<characters>"    Type <characters> into the terminal with a
#                                   <time> delay between each character
#
# Keys:
#   Escape[@<time>] [number]        Press the Escape key
#   Backspace[@<time>] [number]     Press the Backspace key
#   Delete[@<time>] [number]        Press the Delete key
#   Insert[@<time>] [number]        Press the Insert key
#   Down[@<time>] [number]          Press the Down key
#   Enter[@<time>] [number]         Press the Enter key
#   Space[@<time>] [number]         Press the Space key
#   Tab[@<time>] [number]           Press the Tab key
#   Left[@<time>] [number]          Press the Left Arrow key
#   Right[@<time>] [number]         Press the Right Arrow key
#   Up[@<time>] [number]            Press the Up Arrow key
#   Down[@<time>] [number]          Press the Down Arrow key
#   PageUp[@<time>] [number]        Press the Page Up key
#   PageDown[@<time>] [number]      Press the Page Down key
#   Ctrl+<key>                      Press the Control key + <key> (e.g. Ctrl+C)
#
# Display:
#   Hide                            Hide the subsequent commands from the output
#   Show                            Show the subsequent commands in the output

Set WindowBar Colorful
Set Theme "Dracula"
Set BorderRadius 10

Output docs/img/welcome.gif

Require echo
Require banshee
Require jq

Set Shell "zsh"
Set TypingSpeed 60ms
Set FontSize 18
Set Width 1300
Set Height 750

Hide
Type "export PS1='> '" Enter
Type "clear" Enter
Show


Type "Welcome to PS Banshee!" Sleep 1.2 Ctrl+U
Type "banshee" Sleep 0.5s Enter Sleep 1.2s

Type "Lets enrich an IP address with threat intelligence" Sleep 1.5 Ctrl+U
Type "banshee ioc lookup ip 116.198.233.179 -pa" Enter Sleep 2.5s

Type "What about piping raw results?" Sleep 1.5s Ctrl+U 
Type "banshee ioc lookup ip 116.198.233.179 | jq '.[0].risk | {score, risk_rules: [.evidenceDetails[].rule]}'" Enter Sleep 2.5s

Type "Next let's search for Ransomware related sigma rules created in the last 20 days" Sleep 1.5s Ctrl+U
Type "banshee rules search -t sigma --title Ransomware -a 20d -p" Enter Sleep 2.5s

Type "Finally bulk add CVEs from a file to a Vulnerability Watch List" Sleep 1.5s Ctrl+U 
Type "banshee list bulk-add uHHpjf < cve.csv" Enter Sleep 8s