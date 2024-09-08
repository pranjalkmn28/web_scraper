import json
import os
import aiofiles
import aiohttp

class Database:
    @staticmethod
    async def save_to_json(data, file_path='output/products.json'):
        """Save data to a JSON file asynchronously."""
        # Debugging: Print the file_path
        if not file_path:
            raise ValueError("The file_path cannot be empty.")
        
        # Ensure the directory exists
        directory = os.path.dirname(file_path)
        if not directory:
            raise ValueError("The directory part of the file_path cannot be empty.")
        
        os.makedirs(directory, exist_ok=True)
        
        async with aiofiles.open(file_path, 'w') as f:
            await f.write(json.dumps(data, indent=4))

    @staticmethod
    async def download_image(url, save_dir='images'):
        """Download an image from a URL and save it locally asynchronously."""
        os.makedirs(save_dir, exist_ok=True)
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                img_data = await response.read()
                filename = os.path.basename(url)
                image_path = os.path.join(save_dir, filename)
                async with aiofiles.open(image_path, 'wb') as f:
                    await f.write(img_data)
        return image_path