from text_to_image import texttoimage
from customtkinter import *
from tkinter import *
import webbrowser
from PIL import Image
import os, sys
from stability_sdk import client
import stability_sdk.interfaces.gooseai.generation.generation_pb2 as generation
import api as ap

api=ap.api_key_stability



root = CTk()  # create CTk window like you do with the Tk window
root.title("Stability-CTK")
set_appearance_mode("dark")  # Modes: system (default), light, dark  # Themes: blue (default), dark-blue, green

root.geometry()



prompt_str=StringVar(value="")
seed=IntVar(value=4253978046)
steps=IntVar(value=50)
cfg_scale=DoubleVar(value=8.0)
samples=IntVar(value=1)


models=['stable-diffusion-v1',
'stable-diffusion-v1-5',
'stable-diffusion-512-v2-0',
'stable-diffusion-768-v2-0',
'stable-diffusion-512-v2-1',
'stable-diffusion-768-v2-1',
'stable-inpainting-v1-0',
'stable-inpainting-512-v2-0',
'esrgan-v1-x2plus',
'stable-diffusion-xl-beta-v2-2-2',
'stable-diffusion-xl-1024-v0-9',
'stable-diffusion-xl-1024-v1-0',
'stable-diffusion-x4-latent-upscaler',
]

samplers_list=['DDIM',
'PLMS',
'K_EULER',
'K_EULER_ANCESTRAL',
'K_HEUN',
'K_DPM_2',
'K_DPM_2_ANCESTRAL',
'K_DPMPP_2S_ANCESTRAL',
'K_DPMPP_2M',
'K_DPMPP_SDE']

sizes=[
'1024x1024',
'1152x896',
'896x1152',
'1216x832',
'832x1216',
'1344x768',
'768x1344',
'1536x640',
'640x1536',
'512x512'
]

WIDTH_MONITOR = root.winfo_screenwidth()
HEIGHT_MONITOR = root.winfo_screenheight()



main_image=Image.open("img/image.png")

width_photo, height_photo = main_image.size
main_image = main_image.resize((width_photo//2, height_photo//2)) ## The (250, 250) is (height, width)
main_image.save('img/temp.png')
main_image = PhotoImage(file="img/temp.png")

def choise_dir():
    global pathimg
    pathimg = filedialog.askdirectory()

def generate():
    global main_image
    (width, height) = (width_entry.get()).split('x')
    texttoimage(api=api,
                prompt=prompt_entry.get(),
                engine=model_combo.get(),
                seed=int(seed_entry.get()),
                steps=int(steps_entry.get()),
                cfg_scale=float(cfg_scale_entry.get()),
                width=int(width),
                height=int(height),
                samples=int(samples_entry.get()),
                sampler=exec('generation.SAMPLER_' + str(sampler_combo.get())),
                path=pathimg)

    main_image = Image.open(f"{pathimg}/{seed_entry.get()}.png")

    width_photo, height_photo = main_image.size
    main_image = main_image.resize((width_photo // 2, height_photo // 2))  ## The (250, 250) is (height, width)
    main_image.save('img/tempimg.png')
    main_image = PhotoImage(file="img/tempimg.png")
    image_mega.configure(image=main_image)


set_default_color_theme("dark-blue")  # Themes: "blue" (standard), "green", "dark-blue"
root.geometry()

root.option_add("*tearOff", FALSE)

label_model=CTkLabel(root, text='Model: \nSet the engine to use for generation.', justify=LEFT)
label_model.grid(column=0, row=0)

model_combo = CTkComboBox(root, values=models, width=220, height=27)
model_combo.grid(column=0, row=1)


label_prompt=CTkLabel(root, text='Prompt: \nYour response to Stability-CTK', justify=LEFT)
label_prompt.grid(column=0, row=2)

prompt_entry = CTkEntry(root, textvariable=prompt_str, width=220, height=27)
prompt_entry.grid(column=0, row=3)

label_seed=CTkLabel(root, text='Seed: \nIf a seed is provided, the resulting \ngenerated image will be deterministic.', justify=LEFT)
label_seed.grid(column=0, row=4)

seed_entry = CTkEntry(root, textvariable=seed, width=220, height=27)
seed_entry.grid(column=0, row=5)

label_steps=CTkLabel(root, text='Steps: \nAmount of inference steps performed \non image generation.', justify=LEFT)
label_steps.grid(column=0, row=6)

steps_entry = CTkEntry(root, textvariable=steps, width=220, height=27)
steps_entry.grid(column=0, row=7)

label_cfg_scale=CTkLabel(root, text='cfg_scale: \nInfluences how strongly your generation\nis guided to match your prompt.', justify=LEFT)
label_cfg_scale.grid(column=0, row=8)

cfg_scale_entry = CTkEntry(root, textvariable=cfg_scale, width=220, height=27)
cfg_scale_entry.grid(column=0, row=9)

label_width=CTkLabel(root, text='Size: \nSize finish image (width x heihgt)', justify=LEFT)
label_width.grid(column=1, row=0)

width_entry = CTkComboBox(root, values=sizes, width=220, height=27)
width_entry.grid(column=1, row=1)

label_samples=CTkLabel(root, text='Samples: \nNumber of images to generate, defaults\nto 1 if not included.', justify=LEFT)
label_samples.grid(column=1, row=2)

samples_entry = CTkEntry(root, textvariable=samples, width=220, height=27)
samples_entry.grid(column=1, row=3)

label_sampler=CTkLabel(root, text='Sampler: \nChoose which sampler we want to\ndenoise our generation with.', justify=LEFT)
label_sampler.grid(column=1, row=4)

sampler_combo = CTkComboBox(root, values=samplers_list, width=220, height=27)
sampler_combo.grid(column=1, row=5)

save_btn = CTkButton(root, text="Choose save directory", width=220, height=40, command=choise_dir)
save_btn.grid(column=1, row=6)

api_btn = CTkButton(root, text="API KEY", width=110, height=27, command=lambda: os.system("api.py"))
api_btn.grid(column=1, row=7, sticky=W)

btn = CTkButton(root, text="By Bolgaro4ka", width=110, height=27, command= lambda: webbrowser.open("https://github.com/bolgaro4ka", new=1))
btn.grid(column=1, row=7, sticky=E)

generate_btn = CTkButton(root, text="Generate", width=220, height=67, fg_color='green', hover_color='#005500', command=generate)
generate_btn.grid(column=1, row=8, rowspan=2)

image_label=CTkLabel(root, text="Image: ")
image_label.grid(column=2, row=0)

image_mega=CTkLabel(root, text="", image=main_image)
image_mega.grid(column=2, row=1, columnspan=100, rowspan=100)
root.mainloop()
