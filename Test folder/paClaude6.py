import tkinter as tk
from tkinter import ttk, Text
from PIL import Image, ImageTk
import os
import json

class ImageAnnotator:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Annotator")
        
        # Store images and comments
        self.image_files = []
        self.comments = {}
        self.current_index = 0
        self.comments_file = "image_comments.json"
        
        # Fixed display height for all images
        self.display_height = 400
        self.min_width = 300  # Minimum width for the frame
        
        # Get all image files in current directory
        valid_extensions = ('.png', '.jpg', '.jpeg', '.gif', '.bmp')
        self.image_files = [f for f in os.listdir('.') if f.lower().endswith(valid_extensions)]
        
        # Load existing comments if available
        self.load_comments()
        
        if not self.image_files:
            tk.Label(root, text="No images found in current directory!").pack()
            return
            
        # Create GUI elements
        self.create_widgets()
        self.load_current_image()
        
    def load_comments(self):
        """Load comments from JSON file if it exists"""
        try:
            if os.path.exists(self.comments_file):
                with open(self.comments_file, 'r', encoding='utf-8') as f:
                    self.comments = json.load(f)
        except Exception as e:
            print(f"Error loading comments: {e}")
            self.comments = {}
            
    def save_comments_to_file(self):
        """Save comments to JSON file"""
        try:
            with open(self.comments_file, 'w', encoding='utf-8') as f:
                json.dump(self.comments, f, ensure_ascii=False, indent=4)
        except Exception as e:
            print(f"Error saving comments: {e}")
        
    def create_widgets(self):
        # Main container frame
        main_frame = ttk.Frame(self.root)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Frame for image with fixed size
        self.image_frame = ttk.Frame(main_frame, height=self.display_height, width=self.min_width)
        self.image_frame.pack(fill=tk.BOTH, expand=True)
        self.image_frame.pack_propagate(False)  # Prevent frame from shrinking
        
        # Image display
        self.image_label = ttk.Label(self.image_frame)
        self.image_label.pack(fill=tk.BOTH, expand=True)
        
        # Comment box
        self.comment_box = Text(main_frame, height=5, width=50)
        self.comment_box.pack(fill=tk.X, pady=10)
        
        # Navigation buttons
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(pady=10)
        
        ttk.Button(button_frame, text="Previous", command=self.prev_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Next", command=self.next_image).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Done", command=self.generate_html).pack(side=tk.LEFT, padx=5)
        
    def resize_image(self, image):
        # Calculate width while maintaining aspect ratio for fixed height
        ratio = self.display_height / image.height
        display_width = int(image.width * ratio)
        
        # Ensure minimum width
        display_width = max(display_width, self.min_width)
        
        # Resize image
        return image.resize((display_width, self.display_height), Image.Resampling.LANCZOS)
        
    def load_current_image(self):
        # Load and display image
        image_path = self.image_files[self.current_index]
        image = Image.open(image_path)
        
        # Resize image
        resized_image = self.resize_image(image)
        photo = ImageTk.PhotoImage(resized_image)
        
        # Update frame size to match image
        self.image_frame.configure(width=max(resized_image.width, self.min_width))
        self.image_label.configure(image=photo)
        self.image_label.image = photo  # Keep a reference
        
        # Update window title with current image name
        self.root.title(f"Image Annotator - {image_path}")
        
        # Clear comment box
        self.comment_box.delete(1.0, tk.END)
        
        # If this image has a previous comment, load it
        if image_path in self.comments:
            self.comment_box.insert(1.0, self.comments[image_path])
            
    def save_current_comments(self):
        if self.image_files:
            current_image = self.image_files[self.current_index]
            current_comment = self.comment_box.get(1.0, tk.END.strip())
            if current_comment:  # Only save if there's actually a comment
                self.comments[current_image] = current_comment
            self.save_comments_to_file()  # Save to file after each comment update
            
    def next_image(self):
        if self.current_index < len(self.image_files) - 1:
            self.save_current_comments()  # Save current comments before moving
            self.current_index += 1
            self.load_current_image()
            
    def prev_image(self):
        if self.current_index > 0:
            self.save_current_comments()  # Save current comments before moving
            self.current_index -= 1
            self.load_current_image()
            
    def generate_html(self):
        self.save_current_comments()  # Save final comments
        
        html_content = """
        <!DOCTYPE html>
        <html>
        <head>
            <style>
                .image-container {
                    margin: 20px auto;
                    max-width: 800px;
                }
                .comment-box {
                    width: 500px;
                    margin: 10px auto;
                    padding: 10px;
                    border: 1px solid #ccc;
                    white-space: pre-wrap;
                    min-height: 20px;
                }
                img {
                    width: 500px;
                    height: auto;
                    display: block;
                    margin: 0 auto;
                }
            </style>
        </head>
        <body>
        """
        
        # Include all images, with comments if they exist
        for image_file in self.image_files:
            comment = self.comments.get(image_file, "").strip()
            html_content += f"""
            <div class="image-container">
                <img src="{image_file}" alt="{image_file}">
                <div class="comment-box">{comment}</div>
            </div>
            """
            
        html_content += """
        </body>
        </html>
        """
        
        with open("gallery.html", "w", encoding="utf-8") as f:
            f.write(html_content)
            
        self.root.quit()

# Create and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageAnnotator(root)
    root.mainloop()