import os
import shutil
from block import markdown_to_html_node


def extract_title(markdown):
    for line in markdown.splitlines():
        if line.startswith('# '):
            return line[2:].strip()
    raise ValueError("Title must have h1 tag")


def recursive_copy(src, dst):
    if os.path.exists(dst):
        shutil.rmtree(dst)
    os.makedirs(dst)
    log = []

    def copy_contents(src_dir, dst_dir):
        for item in os.listdir(src_dir):
            s = os.path.join(src_dir, item)
            d = os.path.join(dst_dir, item)

            if os.path.isdir(s):
                os.makedirs(d, exist_ok=True)
                log.append(f"Directory created: {d}")
                copy_contents(s, d)
            else:
                shutil.copy2(s, d)
                log.append(f"File copied: {s} to {d}")

    copy_contents(src, dst)
    for entry in log:
        print(entry)


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {
          dest_path} using {template_path}")

    with open(from_path) as rfp:
        fp = rfp.read()

    with open(template_path) as rtp:
        tp = rtp.read()

    html_node = markdown_to_html_node(fp)
    content = html_node.to_html()
    title = extract_title(fp)

    new_content = tp.replace("{{ Title }}", title).replace(
        "{{ Content }}", content)

    os.makedirs(os.path.dirname(dest_path), exist_ok=True)

    with open(dest_path, 'w') as file:
        file.write(new_content)

    return None


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):

    for item in os.listdir(dir_path_content):

        item_path = os.path.join(dir_path_content, item)

        if os.path.isfile(item_path) and item_path.endswith(".md"):

            with open(item_path) as item_p:
                md_file = item_p.read()

            title = extract_title(md_file)
            html_n = markdown_to_html_node(md_file)
            content = html_n.to_html()

            with open(template_path) as item_t:
                t_path = item_t.read()

            rel_path = os.path.relpath(item_path, dir_path_content)
            dest_path = os.path.join(dest_dir_path, rel_path)
            dest_path = dest_path.replace('.md', '.html')
            new_html = t_path.replace("{{ Title }}", title).replace(
                "{{ Content }}", content)

            os.makedirs(os.path.dirname(dest_path), exist_ok=True)

            with open(dest_path, 'w') as dest_file:
                dest_file.write(new_html)

        elif os.path.isdir(item_path):
            new_dest_dir = os.path.join(dest_dir_path, item)
            os.makedirs(new_dest_dir, exist_ok=True)
            generate_pages_recursive(item_path, template_path, new_dest_dir)

    return None


def main():
    recursive_copy('static', 'public')
    generate_pages_recursive(
        'content/', 'template.html', 'public/')


main()
