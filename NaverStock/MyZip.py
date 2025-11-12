import os
import zipfile


# Directoy to Zip File
def folder_to_zip(folder_path, output_zip_path) :

    if not os.path.isdir(folder_path):
        print(f"❌ 오류: 지정된 폴더 경로가 유효하지 않거나 존재하지 않습니다: {folder_path}")
        return
    
    if os.path.exists(output_zip_path) :
        os.remove(output_zip_path)
  
    with zipfile.ZipFile(output_zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
        
        # get path, sub directory, sub files
        for root, dirs, files in os.walk(folder_path):
            # get relative path
            archive_root = os.path.relpath(root, folder_path)
    
            for file in files:
                file_path = os.path.join(root, file)
                archive_name = os.path.join(archive_root, file)

                zipf.write(file_path, archive_name)
                print(f"압축 완료: {archive_name}")

    print(f"\n🎉 폴더 압축이 완료되었습니다. 생성된 파일: {output_zip_path}")
    

if __name__ == "__main__" :
    current_path = os.path.dirname(os.path.abspath(__file__))
    folder_path = current_path + "\\reports"
    output_zip_path = current_path + "\\reports.zip"
    
    folder_to_zip(folder_path, output_zip_path)