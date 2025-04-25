
import os
from PIL import Image
import UnityPy
from UnityPy.classes import Texture2D
from UnityPy.enums import TextureFormat as TF


ab_dir_path = './data_out' # hpb unpack output dir
img_dir_path = './img'     # replace image dir

for ab_name in os.listdir(ab_dir_path):
    ab_path = os.path.join(ab_dir_path, ab_name)
    if os.path.isfile(ab_path):
        
        need_save = False
        env = UnityPy.load(ab_path)
        print(f"Loading AssetBundle {ab_name}...")
        for obj in env.objects:
            if obj.type.name == "Texture2D":
                data: Texture2D = obj.read() # type: ignore
                
                name = data.m_Name
                img_path = os.path.join(img_dir_path, name) + ".png"
                if not os.path.isfile(img_path):
                    img_path = os.path.join(img_dir_path, name) + ".jpg"
                if not os.path.isfile(img_path):
                    img_path = None
                
                if img_path:
                    img = Image.open(img_path)
                    data.set_image(img, target_format=TF.DXT1)
                    data.save()
                    print(f"{img_path} saved to {name}")
                    need_save = True
                else:
                    # print(f"Image {name} not found")
        
        if need_save:
            with open(ab_path, "wb") as f:
                f.write(env.file.save()) # type: ignore
            print(f"AssetBundle {ab_name} saved")
        print()