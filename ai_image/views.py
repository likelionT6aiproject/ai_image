from django.shortcuts import render, redirect, get_object_or_404
from django.core.files.base import ContentFile
from .forms import ImageUploadForm
from .models import UploadedImage
from PIL import Image
import io
import torch
from diffusers import StableDiffusionInstructPix2PixPipeline, EulerAncestralDiscreteScheduler
from django.http import JsonResponse

def transform_image(image_file, prompt):
    model_id = "timbrooks/instruct-pix2pix"
    pipe = StableDiffusionInstructPix2PixPipeline.from_pretrained(model_id, torch_dtype=torch.float16, safety_checker=None)
    pipe.to("cuda")
    pipe.scheduler = EulerAncestralDiscreteScheduler.from_config(pipe.scheduler.config)
    
    image = Image.open(image_file)
    images = pipe(prompt, image=image, num_inference_steps=10, image_guidance_scale=1).images
    transformed_image = images[0]
    
    buffer = io.BytesIO()
    transformed_image.save(buffer, format="PNG")
    return buffer.getvalue()

def upload_image(request):
    if request.method == 'POST':
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_image = form.save(commit=False)
            prompt = form.cleaned_data['prompt']
            transformed_image_data = transform_image(request.FILES['image'], prompt)

            # Save original image
            uploaded_image.image = request.FILES['image']

            # Save transformed image
            transformed_image_name = 'transformed_image.png'
            uploaded_image.transformed_image.save(transformed_image_name, ContentFile(transformed_image_data), save=False)

            # Save the uploaded image instance
            uploaded_image.save()

            # Return JSON response with transformed image URL
            return JsonResponse({'image_url': uploaded_image.transformed_image.url})
    else:
        form = ImageUploadForm()

    return render(request, 'upload.html', {'form': form})

def view_result(request, pk):
    image = get_object_or_404(UploadedImage, pk=pk)
    return render(request, 'result.html', {'image': image})

