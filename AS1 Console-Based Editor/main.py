import re
#?    - display this help info(显示帮助信息)
def dispiay_help_info():
    print(
    """
    ? - display this help info
    h - move cursor left
    l - move cursor right
    . - toggle row cursor on and off
    ^ - move cursor to beginning of the line
    $ - move cursor to end of the line
    w - move cursor to beginning of next word
    b - move cursor to beginning of current or previous word
    e - move cursor to end of the word
    i - insert <text> before cursor
    a - append <text> after cursor
    I - insert <text> from beginning
    A - append <text> at the end
    x - delete character at cursor
    X - delete character before cursor
    v - view editor content
    q - quit program
    """
    )
#. - toggle row cursor on and off (开启/关闭光标高亮)
def switch_cursor_highlight():
    global cursor_highlight
    cursor_highlight = not cursor_highlight
    view_editor_content()
#h - move cursor left(光标向左移动)
def move_cursor_left():
    global cursor_position
    if cursor_position > 0:
        cursor_position -= 1
    view_editor_content()
#l - move cursor right(光标向右移动)
def move_cursor_right():
    global content,cursor_position
    if cursor_position < len(content) - 1:
        cursor_position += 1
    view_editor_content()
#^ - move cursor to beginning of the line (移动到行首)
def cursor_to_linehead():
    global content,cursor_position
    cursor_position = 0
    view_editor_content()
#$ - move cursor to end of the line (移动到行尾)
def cursor_to_linetail():
    global content,cursor_position
    cursor_position = len(content) - 1
    view_editor_content()
#w - move cursor to beginning of next word (移动到下一个单词开头)
def cursor_to_nextword_head():
    global content,cursor_position
    while ord(content[cursor_position]) != 32 and cursor_position < len(content)-1:
        cursor_position += 1
    if cursor_position < len(content)-1:
        cursor_position += 1
    view_editor_content()
#b - move cursor to beginning of current or previous word(移动到当前或前一个单词开头)
def cursor_to_currentword_or_previousword_head():
    global content,cursor_position
    if ord(content[cursor_position-1]) == 32:
        cursor_position -= 1
    while cursor_position >0 and ord(content[cursor_position-1]) != 32:
        cursor_position -= 1
    view_editor_content()
#e - move cursor to end of current or next word (移动到单词末尾)
def cursor_to_currentword_or_nextword_tail():
    global content,cursor_position
    try:
        if ord(content[cursor_position+1]) == 32:
            cursor_position += 1
        while cursor_position < len(content)-1 and ord(content[cursor_position+1]) != 32:
            cursor_position += 1
        view_editor_content()
    except IndexError:
        cursor_to_linetail()
#i - insert <text> before cursor (在光标前插入文本)
def insert_before_cursor(text):
    global content,cursor_position
    if len(content) == 0:
        insert_from_beginning(text)
    else:
        content = content[:cursor_position:] + text + content[cursor_position::]
        view_editor_content()
#a - append <text> after cursor (在光标后追加文本)
def append_after_cursor(text):
    global content,cursor_position
    if len(content) == 0:
        append_at_the_end(text)
    else:
        content = content[:cursor_position+1:] + text + content[cursor_position+1 ::]
        view_editor_content()
#I - insert <text> from beginning (在行首插入文本)
def insert_from_beginning(text):
    global content
    content = text + content
    cursor_to_linehead()
#A - append <text> at the end (在行尾追加文本)
def append_at_the_end(text):
    global content
    content = content + text
    cursor_to_linetail()
#x - delete character at cursor (删除光标处字符)
def delete_character_at_cursor():
    global cursor_position,content
    content = content[:cursor_position:] + content[cursor_position+1::]
    if len(content)-1 < cursor_position:
        cursor_position -= 1
    view_editor_content()
#X - delete character before cursor (删除光标前一个字符)
def delete_character_before_cursor():
    global cursor_position,content
    if cursor_position == 0:
        pass
    else:
        content = content[:cursor_position-1:] + content[cursor_position::]
        cursor_position -= 1
    view_editor_content()
#v - view editor content (查看编辑器内容)
def view_editor_content():
    global cursor_highlight,content
    if len(content) == 0:
        print()
        return
    if cursor_highlight == True:
        print(content[:cursor_position:] +
        "\033[42m" + content[cursor_position] + "\033[0m" +
        content[cursor_position+1 ::])
    else:
        print(content)
#analyse user input
def parse_command(user_input):
    pattern = r"^([?.hl^$wbeiaIAxXvq])(.*)$"
    match = re.match(pattern,user_input)
    if not match:
        return None,None
    cmd,text = match.groups()
    if (cmd in "iaIA" and not text) or (cmd not in "iaIA" and text):
        return None,None
    else:
        return cmd,text
#q - quit program (退出程序)
content = ""
cursor_position = None
cursor_highlight = True
user_input = input(">")
while user_input != "q":
    cmd , text = parse_command(user_input)
    if cmd == "?":
        dispiay_help_info()
    elif cmd == ".":
        switch_cursor_highlight()
    elif cmd == "h":
        move_cursor_left()
    elif cmd == "l":
        move_cursor_right()
    elif cmd == "^":
        cursor_to_linehead()
    elif cmd == "$":
        cursor_to_linetail()
    elif cmd == "w":
        cursor_to_nextword_head()
    elif cmd == "b":
        cursor_to_currentword_or_previousword_head()
    elif cmd == "e":
        cursor_to_currentword_or_nextword_tail()
    elif cmd == "i":
        insert_before_cursor(text)
    elif cmd == "a":
        append_after_cursor(text)
    elif cmd == "I":
        insert_from_beginning(text)
    elif cmd == "A":
        append_at_the_end(text)
    elif cmd == "x":
        delete_character_at_cursor()
    elif cmd == "X":
        delete_character_before_cursor()
    elif cmd == "v":
        view_editor_content()
    user_input = input(">")
