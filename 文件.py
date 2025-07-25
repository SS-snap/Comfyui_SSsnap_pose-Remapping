import os

def print_tree(startpath, indent=''):
    for entry in os.scandir(startpath):
        if entry.is_dir():
            print(f"{indent}{entry.name}/")
            print_tree(entry.path, indent + '    ')
        else:
            print(f"{indent}{entry.name}")

if __name__ == "__main__":
    base = r"F:\AI\comfyui\ComfyUI_windows_portable\ComfyUI\custom_nodes\comfyui_poseremapping"  # 改成你的路径
    print_tree(base)