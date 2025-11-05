import tkinter as tk
from tkinter import ttk, scrolledtext
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse

class WebScraperApp:
    def __init__(self, root):
        self.root = root
        self.root.title("采集网址工具")
        
        # 创建界面组件
        self.create_widgets()

        # 居中显示窗口
        self.center_window()
    
    def create_widgets(self):
        # 输入URL框架
        input_frame = ttk.Frame(self.root, padding=10)
        input_frame.pack(fill=tk.X)
        
        ttk.Label(input_frame, text="输入网页URL:").pack(side=tk.LEFT)
        
        self.url_entry = ttk.Entry(input_frame, width=40)
        self.url_entry.pack(side=tk.LEFT, padx=5)
        
        self.fetch_btn = ttk.Button(input_frame, text="获取内容", command=self.fetch_content)
        self.fetch_btn.pack(side=tk.LEFT)
        
        self.clear_btn = ttk.Button(input_frame, text="清空", command=self.clear_content)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
        
        # 结果显示区域
        result_frame = ttk.Frame(self.root)
        result_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        self.result_text = scrolledtext.ScrolledText(result_frame, wrap=tk.WORD)
        self.result_text.pack(fill=tk.BOTH, expand=True)

        # 添加底部版权信息
        self.copyright_frame = tk.Frame(self.root, bg="yellow")
        self.copyright_frame.pack(fill="x", side="bottom", pady=5)

        copyright_text = "版权所有：速光网络软件开发，抖音号：dubaishun12"
        self.copyright_label = tk.Label(
            self.copyright_frame,
            text=copyright_text,
            bg="yellow",
            font=("微软雅黑", 10)
        )
        self.copyright_label.pack(expand=True)
    
    def fetch_content(self):
        url = self.url_entry.get().strip()
        if not url:
            self.show_message("请输入有效的URL地址")
            return
        
        try:
            # 发送HTTP请求
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            
            # 解析HTML内容
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # 提取标题和链接（可根据实际网页结构调整选择器）
            links = []
            
            # 提取<a>标签的文本内容（标题）和链接（href）
            for link_tag in soup.find_all('a', href=True):
                title = link_tag.get_text(strip=True)
                href = link_tag['href']
                
                # 处理相对路径
                parsed_url = urlparse(url)
                base_url = f"{parsed_url.scheme}://{parsed_url.netloc}"
                if not href.startswith(('http://', 'https://')):
                    href = f"{base_url}/{href.lstrip('/')}"
                
                # 存储标题和链接
                links.append((title, href))
            
            # 显示结果
            result = "找到的内容：\n\n"
            result += "链接列表：\n"
            for title, link in links:
                result += f"- {title}: {link}\n"
            
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, result)
            
        except requests.exceptions.RequestException as e:
            self.show_message(f"请求错误: {str(e)}")
        except Exception as e:
            self.show_message(f"发生错误: {str(e)}")

    def show_message(self, message):
        self.result_text.delete(1.0, tk.END)
        self.result_text.insert(tk.END, message)
    
    def clear_content(self):
        # 清空输入框和显示区域
        self.url_entry.delete(0, tk.END)
        self.result_text.delete(1.0, tk.END)

    def center_window(self):
        # 在控件布局完成后计算窗口大小并居中
        self.root.update_idletasks()

        width = self.root.winfo_width()
        height = self.root.winfo_height()

        # 初始宽高可能为1，回退到推荐尺寸或所需尺寸
        if width <= 1 or height <= 1:
            width = max(self.root.winfo_reqwidth(), 800)
            height = max(self.root.winfo_reqheight(), 600)

        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()

        x = (screen_width - width) // 2
        y = (screen_height - height) // 2

        self.root.geometry(f"{width}x{height}+{x}+{y}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WebScraperApp(root)
    root.mainloop()
