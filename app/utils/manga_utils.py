def get_folder_name(manga_name, chapter_number):
    folder_name = manga_name.lower().replace(" ", "_")
    print("save in folder: " + folder_name)
    return f"mangas/{folder_name}/{chapter_number}"
