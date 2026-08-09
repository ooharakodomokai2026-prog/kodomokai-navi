function doPost(e) {
  try {
    var mainFolderId = "1l9SzYOf0p4W08Wmv7x8f1kpSArjMAjmx";
    var mainFolder = DriveApp.getFolderById(mainFolderId);
    
    var data = JSON.parse(e.postData.contents);
    var targetYear = data.year + "年";
    var targetMonth = data.month;
    
    // 年フォルダの有無をチェックし、なければ自動作成
    var subFolders = mainFolder.getFoldersByName(targetYear);
    var yearFolder = subFolders.hasNext() ? subFolders.next() : mainFolder.createFolder(targetYear);
    
    // ファイル名の先頭に【〇月提出】を付与
    var newFileName = "【" + targetMonth + "提出】" + data.fileName;
    
    var bytes = Utilities.base64Decode(data.fileData);
    var blob = Utilities.newBlob(bytes, data.mimeType, newFileName);
    var file = yearFolder.createFile(blob);
    
    return ContentService.createTextOutput(JSON.stringify({"result": "success", "fileId": file.getId()}))
      .setMimeType(ContentService.MimeType.JSON);
  } catch(err) {
    return ContentService.createTextOutput(JSON.stringify({"result": "error", "error": err.toString()}))
      .setMimeType(ContentService.MimeType.JSON);
  }
}
