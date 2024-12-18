import sys,os
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from PIL import Image, ImageTk
from tkinterdnd2 import DND_FILES, TkinterDnD

class ICO_CNVER(TkinterDnD.Tk):
    """
    아이콘 변환 프로그램
    이미지 파일을 드래그앤드롭 해서 ICO 파일로 변환하는 기능
    
    1. 이미지 입력 ZONE에 이미지를 끌어다 놓는다.
    2. ICO 파일이 이미지 파일과 같은 경로에 생성된다. 
    """

    def __init__(self, config):
        """
        프로그램 초기화 초기화 메소드
        
        Args:
            self (ICO_CONVERTER Object)
            config (dictionary) : 프로그램 설정값

        Returns:
            ICO_CONVERTER Object
        """
        super().__init__()
        self.outputPath = "./output/"
        self.config = config  # 설정 값 저장

    def initDragAndDropZone(self):
        """
        드래그 앤 드랍 zone 설정 메소드
        
        드래그 앤 드랍기능으로 사용할 컨트롤러 설정을 진행한다.

        Args:
            self (ICO_CONVERTER Object)
        Returns:
        """
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

    def initPreviewImageView(self):
        """
        이미지 미리보기 컨트롤 설정 메소드
        
        입력된 이미지 파일을 표시할 컨트롤을 설정한다.

        Args:
            self (ICO_CONVERTER Object)
        Returns:
        """
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
        """
        에러메시지 출력 메소드

        에러메시지를 이미지 출력 컨트롤에 출력한다.
        
        Args:
            self (ICO_CONVERTER Object)
            msg (string)    : 에러메시지

        Returns:
        """
        self.image_label.config(text=msg, bootstyle="danger")

    def displayImage(self, target, file_path):
        """
        이미지 출력 메소드

        이미지를 로딩하여 리사이즈 한 후 미리보기 컨트롤에 출력한다.
        
        Args:
            self (ICO_CONVERTER Object)
            target (Object)     : 이미지를 출력할 객체
            file_path (string)  : 이미지 파일 경로

        Returns:
        """
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
            self.image_label.config(text=f"Error loading image: \r\n{e}")

    def on_drop(self, event):
        """
        <<DROP>>> 이벤트 처리 함수

        파일 DROP 이벤트 발생할시 파일 경로 및 ICO 파일로 컨버팅을 실행한다.
        
        Args:
            self (ICO_CONVERTER Object)
            target (Object)     : 이미지를 출력할 객체
            file_path (string)  : 이미지 파일 경로

        Returns:
        """
        # 드롭된 파일 경로 처리
        files = self.split_files(event.data)
        if len(files) > 1:
            self.showImageLoadingError("Please drop only one file.")
        else:
            file_path = files[0]

            if not file_path.lower().endswith((".png", ".jpg", ".jpeg", ".webp")):
                self.showImageLoadingError("Invalid file type.\r\nPlease drop an image.")
                return
            
            self.displayImage(self.image_label, file_path=file_path)
            self.convertICO(file_path)
      
    @staticmethod
    def split_files(file_string):
        """
        파일 목록 split 메소드

        입력된 파일 목록을 split하여 배열로 반환한다.

        Args:
            self (ICO_CONVERTER Object)
            target (Object)     : 이미지를 출력할 객체
            file_path (string)  : 이미지 파일 경로

        Returns:
            파일 목록 배열(array)
        """
        # 여러 파일이 드래그된 경우 처리
        return file_string.split()
    
    @staticmethod    
    def get_resource_path(relative_path):
        """
        PyInstaller에서 리소스 파일의 경로를 가져오는 함수

        Args:
            실제파일 경로(string)
        Returns:
            패키징된 파일 경로(string)
        """
        # PyInstaller로 패키징된 경우
        if hasattr(sys, '_MEIPASS'):
            return os.path.join(sys._MEIPASS, relative_path)
        # 개발 환경에서 실행되는 경우
        else:
            return os.path.join(os.path.abspath("."), relative_path)      

    
    def run(self):
        """
        앱 실행 메소드

        Args:
            self (ICO_CONVERTER Object)
        Returns:
        """
        self.title("ICON CNVER")
        self.geometry("360x160")
        self.minsize(360,160)
        self.maxsize(360,160)

        self.iconbitmap(self.get_resource_path("res/icon_cnver.ico"))

        self.style = ttk.Style(theme="solar")  # 다른 테마로 변경 가능
        
        self.initDragAndDropZone()
        self.initPreviewImageView()

        # APP 실행
        self.mainloop()
    
    def convertICO(self, path):
        """
        앱 실행 메소드

        Args:
            self (ICO_CONVERTER Object)

        Returns:
        """
        directory, file_name = os.path.split(path)
        base_name, extension = os.path.splitext(file_name)
        img = Image.open(path)
        img.save(f"{directory}\\{base_name}.ico", format="ICO", sizes=[(16, 16), (32, 32), (48, 48), (64, 64), (128, 128), (256, 256)])


if __name__ == "__main__":
    config = {"debug": True, "version": "0.0.1"}  # 설정 값
    app = ICO_CNVER(config)
    app.run()

