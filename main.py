import os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD

class Mainframe(TkinterDnD.Tk):
    def __init__(self, config):
        super().__init__()
        self.outputPath = "./output/"
        self.config = config  # 설정 값 저장

    def initDragAndDropZone(self):
        # 파일 드롭 영역
        self.dnd_label = ttk.Label(
            self,
            text="Drag & Drop files here",
            bootstyle="info",
            background="white",
            anchor="center",
            width=20)
        self.dnd_label.pack(side='left', fill="y", anchor="w", padx=20, pady=20)

        # 드래그 앤 드롭 이벤트 연결
        self.dnd_label.drop_target_register(DND_FILES)
        self.dnd_label.dnd_bind('<<Drop>>', self.on_drop)

        # image view
        self.image_label = ttk.Label(
            self, 
            text="No file dropped", 
            bootstyle="info",
            background="white",
            anchor="center",
            width=20)
        self.image_label.pack(side='right', fill="y", anchor="e", padx=20, pady=20)

    def showImageLoadingError(self, msg):
        self.image_label.config(text=msg, bootstyle="danger")

    def displayImage(self, target, file_path):
        """이미지를 로드하고 출력"""
        try:
            # Pillow로 이미지 로드
            image = Image.open(file_path)

            # width = int(image.width * ratio)
            # height = int(image.height * ratio)

            image = image.resize((100, 100), Image.Resampling.LANCZOS)  # 이미지 크기 조정
            photo = ImageTk.PhotoImage(image)

            # ttkbootstrap.Label에 이미지 표시
            target.config(image=photo)
            target.image = photo  # 참조 유지

        except Exception as e:
            print(e)
            self.image_label.config(text=f"Error loading image: \r\n{e}")

    def on_drop(self, event):
        # 드롭된 파일 경로 처리
        files = self.split_files(event.data)
        if len(files) > 1:
            self.showImageLoadingError("Please drop only one file.")
        else:
            file_path = files[0]
            print(file_path)

            if not file_path.lower().endswith((".png", ".jpg", ".jpeg")):
                self.showImageLoadingError("Invalid file type.\r\nPlease drop an image.")
                return
            
            self.displayImage(self.image_label, file_path=file_path)
            self.convertICO(file_path)
            
    @staticmethod
    def split_files(file_string):
        # 여러 파일이 드래그된 경우 처리
        return file_string.split()
    
    def run(self):
        self.title("ICON CONVERTER")
        self.geometry("360x160")
        self.minsize(360,160)
        self.maxsize(360,160)

        self.style = ttk.Style(theme="solar")  # 다른 테마로 변경 가능
        
        self.initDragAndDropZone()
        # self.convPNGtoICO("./resource/space-station.png")

        # APP 실행
        self.mainloop()
    
    def convertICO(self, path):
        directory, file_name = os.path.split(path)
        base_name, extension = os.path.splitext(file_name)
        img = Image.open(path)
        img.save(f"{directory}\\{base_name}.ico")

if __name__ == "__main__":
    config = {"debug": True, "version": "1.0"}  # 설정 값
    app = Mainframe(config)
    app.run()