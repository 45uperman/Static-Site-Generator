import os, shutil
from dependencies.convertable_document import ConvertableDocument

def copy_dir_r(src, dst):
    if os.path.isfile(src):
        print(src)
        shutil.copy(src, dst)
        return
    if os.path.exists(dst) is False:
        os.mkdir(dst)
    for entry in os.listdir(src):
        new_src = os.path.join(src, entry)
        new_dst = os.path.join(dst, entry)
        copy_dir_r(new_src, new_dst)
    return

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as f, open(template_path) as t:
        markdown = f.read(4000000000)
        template = t.read(4000000000)
    document = ConvertableDocument(markdown)
    html = template.replace(r"{{ Title }}", document.html_title).replace(r"{{ Content }}", document.to_html())
    dest_head = os.path.dirname(dest_path)
    if os.path.exists(dest_head) is False:
        os.makedirs(dest_head, exist_ok=True)
    with open(dest_path, "w") as html_file:
        html_file.write(html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    if os.path.isfile(dir_path_content):
        file_name = os.path.split(dir_path_content)[1]
        destination_dir = os.path.dirname(dest_dir_path)
        destination = os.path.join(destination_dir, file_name.replace(".md", ".html"))
        generate_page(dir_path_content, template_path, destination)
        return
    if os.path.exists(dest_dir_path) is False:
        os.mkdir(dest_dir_path)
    for entry in os.listdir(dir_path_content):
        new_content_path = os.path.join(dir_path_content, entry)
        new_dest_path = os.path.join(dest_dir_path, entry)
        print(f"Recursing with new content path: {new_content_path} and new dest path: {new_dest_path}")
        generate_pages_recursive(new_content_path, template_path, new_dest_path)
    return
    

def main():
    # C:\Projects\Static Site Generator\
    static = r"./static"
    public = r"./public"
    content = r"./content"
    template = r"./template.html"
    destination = r"./public/index.html"
    shutil.rmtree(public)
    os.mkdir(public)
    copy_dir_r(static, public)
    generate_pages_recursive(content, template, public)

main()
