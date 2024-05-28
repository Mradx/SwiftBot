import re


def add_missing_delimiters(text: str):
    if text.count("```") % 2 != 0:
        text += "```"
    if text.count("`") % 2 != 0:
        text += "`"
    return text


def replace_block(match, placeholders):
    language = match.group(1) if match.group(1) else ""
    code_content = match.group(3)
    placeholder = f"CODEBLOCKPLACEHOLDER{len(placeholders)}"
    placeholders.append(placeholder)
    if not language:
        html_code_block = f"<pre><code>{code_content}</code></pre>"
    else:
        html_code_block = f'<pre><code class="language-{language}">{code_content}</code></pre>'
    return placeholder, html_code_block


def convert_code_blocks(text: str):
    text = add_missing_delimiters(text)
    placeholders = []
    code_blocks = {}
    modified_text = text
    for match in re.finditer(r"```(\w*)?(\n)?(.*?)```", text, flags=re.DOTALL):
        placeholder, html_code_block = replace_block(match, placeholders)
        code_blocks[placeholder] = html_code_block
        modified_text = modified_text.replace(match.group(0), placeholder, 1)
    return modified_text, code_blocks


def insert_code_blocks(text: str, code_blocks: dict):
    for placeholder, html_code_block in code_blocks.items():
        text = text.replace(placeholder, html_code_block, 1)
    return text


def replace_tags(out_text: str, md_tag: str, html_tag: str) -> str:
    tag_pattern = re.compile(
        r"{}(.*?){}".format(re.escape(md_tag), re.escape(md_tag)), re.DOTALL
    )
    return tag_pattern.sub(r"<{}>\1</{}>".format(html_tag, html_tag), out_text)


def format_text(text: str) -> str:
    output, code_blocks = convert_code_blocks(text)
    output = output.replace("<", "&lt;").replace(">", "&gt;")
    output = re.sub(r"`(.*?)`", r"<code>\1</code>", output)
    output = re.sub(r"\*\*\*(.*?)\*\*\*", r"<b><i>\1</i></b>", output)
    output = replace_tags(output, "**", "b")
    output = replace_tags(output, "__", "u")
    output = replace_tags(output, "_", "i")
    output = replace_tags(output, "*", "i")
    output = replace_tags(output, "~~", "s")
    output = re.sub(r"\[(.*?)\]\((.*?)\)", r'<a href="\2">\1</a>', output)
    output = re.sub(r"^\s*[\-\*] (.+)", r"• \1", output, flags=re.MULTILINE)
    output = re.sub(r"^\s*#+ (.+)", r"<b>\1</b>", output, flags=re.MULTILINE)
    output = insert_code_blocks(output, code_blocks)
    return output
