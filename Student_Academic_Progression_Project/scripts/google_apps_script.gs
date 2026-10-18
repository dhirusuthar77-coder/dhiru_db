/**
 * ==============================================================================
 * STUDENT ACADEMIC PROGRESSION & PORTFOLIO MANAGEMENT SYSTEM (SAPMS)
 * Google Apps Script Web App: Deduplication & Clean Sync
 * File: Code.gs
 * Target Tabs (Only these 8 exact sheets will remain):
 * 1. achievement_categories
 * 2. students
 * 3. school_records
 * 4. semesters
 * 5. subjects
 * 6. semester_results
 * 7. drop_years
 * 8. achievements
 * ==============================================================================
 */

// 1. GET Handler
function doGet(e) {
  var action = (e && e.parameter && e.parameter.action) || 'status';
  if (action === 'clean_duplicates') {
    var count = removeAllDuplicateSheetsAndRows();
    return ContentService.createTextOutput(JSON.stringify({
      status: 'success',
      message: 'Cleaned duplicate sheets and rows successfully!',
      cleaned_info: count
    })).setMimeType(ContentService.MimeType.JSON);
  }

  return ContentService.createTextOutput(JSON.stringify({
    status: 'online',
    system: 'Student Academic Progression System',
    timestamp: new Date().toISOString()
  })).setMimeType(ContentService.MimeType.JSON);
}

// 2. POST Handler: Writes unique data and removes all duplicate sheets/rows
function doPost(e) {
  try {
    if (!e || !e.postData || !e.postData.contents) {
      return ContentService.createTextOutput(JSON.stringify({
        status: 'error',
        message: 'No payload received'
      })).setMimeType(ContentService.MimeType.JSON);
    }

    var payload = JSON.parse(e.postData.contents);
    var ss = SpreadsheetApp.getActiveSpreadsheet();
    var tables = payload.tables || {};

    var targetTabs = [
      'achievement_categories',
      'students',
      'school_records',
      'semesters',
      'subjects',
      'semester_results',
      'drop_years',
      'achievements'
    ];

    // STEP A: Remove any duplicate or legacy sheets (like capitalized 'Students', 'School_Records', 'Attendance', etc.)
    var allSheets = ss.getSheets();
    allSheets.forEach(function(s) {
      var name = s.getName();
      // If the sheet name is NOT one of the exact 8 target tabs, delete it
      if (targetTabs.indexOf(name) === -1) {
        if (ss.getSheets().length > 1) {
          try { ss.deleteSheet(s); } catch (e) {}
        }
      }
    });

    // STEP B: Populate the 8 target sheets with strictly unique rows
    targetTabs.forEach(function(tabName, index) {
      var sheet = ss.getSheetByName(tabName);
      if (!sheet) {
        sheet = ss.insertSheet(tabName);
      }
      sheet.clear();

      // Ensure exact position in tab bar (1 to 8)
      ss.setActiveSheet(sheet);
      ss.moveActiveSheet(index + 1);

      if (tables[tabName]) {
        var headers = tables[tabName].headers || [];
        var rawRows = tables[tabName].rows || [];

        // Deduplicate rows based on JSON string representation
        var uniqueRows = [];
        var seenRows = {};
        for (var i = 0; i < rawRows.length; i++) {
          var rowKey = JSON.stringify(rawRows[i]);
          if (!seenRows[rowKey]) {
            seenRows[rowKey] = true;
            uniqueRows.push(rawRows[i]);
          }
        }

        if (headers.length > 0) {
          // Set Header Styling
          sheet.getRange(1, 1, 1, headers.length)
               .setValues([headers])
               .setBackground('#1e293b')
               .setFontColor('#ffffff')
               .setFontWeight('bold');

          // Set Unique Data Rows
          if (uniqueRows.length > 0) {
            sheet.getRange(2, 1, uniqueRows.length, headers.length).setValues(uniqueRows);
            // Native Google Sheets remove duplicates safeguard
            try {
              sheet.getDataRange().removeDuplicates();
            } catch (err) {}
          }

          sheet.autoResizeColumns(1, headers.length);
        }
      }
    });

    return ContentService.createTextOutput(JSON.stringify({
      status: 'success',
      message: 'All duplicate sheets and rows removed! Cleaned 8 sheets in exact sequence.'
    })).setMimeType(ContentService.MimeType.JSON);

  } catch (err) {
    return ContentService.createTextOutput(JSON.stringify({
      status: 'error',
      message: err.toString()
    })).setMimeType(ContentService.MimeType.JSON);
  }
}

// 3. UI Menu: 1-click duplicate cleaner inside Google Sheets
function onOpen() {
  SpreadsheetApp.getUi()
    .createMenu('🧹 Data Cleaner')
    .addItem('🗑️ Remove All Duplicate Sheets & Rows', 'menuCleanDuplicates')
    .addToUi();
}

function menuCleanDuplicates() {
  removeAllDuplicateSheetsAndRows();
  SpreadsheetApp.getUi().alert('✅ Done: All duplicate sheets and duplicate rows have been removed!');
}

function removeAllDuplicateSheetsAndRows() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  var targetTabs = [
    'achievement_categories',
    'students',
    'school_records',
    'semesters',
    'subjects',
    'semester_results',
    'drop_years',
    'achievements'
  ];

  // Delete all non-target sheets
  var allSheets = ss.getSheets();
  allSheets.forEach(function(s) {
    var name = s.getName();
    if (targetTabs.indexOf(name) === -1) {
      if (ss.getSheets().length > 1) {
        try { ss.deleteSheet(s); } catch (e) {}
      }
    }
  });

  // Remove duplicate rows in each target sheet
  targetTabs.forEach(function(tabName) {
    var sheet = ss.getSheetByName(tabName);
    if (sheet && sheet.getLastRow() > 1) {
      try {
        sheet.getDataRange().removeDuplicates();
      } catch (e) {}
    }
  });
}
