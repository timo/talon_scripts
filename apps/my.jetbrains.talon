# Requires https://plugins.jetbrains.com/plugin/10504-voice-code-idea

app: /jetbrains/

app: IntelliJ IDEA
app: PyCharm
app: PyCharm64.exe
# When tags are supported
#tags: ide
-
match brace: user.idea("action EditorMatchBrace")

jump: user.idea("action com.gitlab.lae.intellij.jump.JumpToChar")
