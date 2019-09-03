import shutil
import os
import openpyxl
from collections import Counter

def main():
    print('\nNOTE: validating spreadsheet against template version 20190724; update script if new template is in use.')
    
    #get a list of barcodes in new spreadsheet inventory
    while True:
        spreadsheet = input('\nEnter Python-appropriate path to the spreadsheet: ')
    
        if os.path.exists(spreadsheet):
            break
    
    wb = openpyxl.load_workbook(spreadsheet)
    ws = wb['Inventory']
    
    #make sure correct column headers are in use
    
    #current column headers--UPDATE IF NEEDED!
    template_headers = ['Identifier', 'Accession ID (if known)', 'Collection Title (if assigned)', 'Collection ID (if assigned)', 'Creator (if known)', 'Physical location of media', 'Source type (select from drop down or type)', 'Label transcription', 'Initial appraisal notes (including potential sensitive data)', 'Instructions for BDPL staff ', 'Restriction Statement', 'Restriction end date (YYYY-MM-DD)', 'Move directly to SDA without appraisal? ']
    
    new_headers = []
    for cell in ws[1]:
        if not cell.value is None:
            new_headers.append(cell.value)
    
    column_list = 'ABCDEFGHIJKLMNOP'
    
    #compare current headers vs. template
    for i in range(0, len(template_headers)):
        if new_headers[i] != template_headers[i]:
            print('\n\nWARNING: Column %s has incorrect header!\n\tHeader is "%s"; SHOULD be "%s"' % (column_list[i], new_headers[i], template_headers[i]))
    
    new_bcs = {}    
    missing_barcodes = []
    
    for barcode in ws['A'][1:]:
        if not barcode.value is None:
            new_bcs[barcode.value] = barcode.row
        else:
            missing_barcodes.append(barcode.row)
    
    #note if any barcode values are missing
    if len(missing_barcodes) > 0:
        print('\n\n\nWARNING: the following rows are missing barcodes; verify if any action is needed:')
        for row in missing_barcodes:
            print('\tRow: %s' % row)
    
    new_bcs_list = list(new_bcs.keys())
    
    #check for any duplicate barcodes in new spreadsheet
    duplicate_barcodes = [item for item, count in Counter(new_bcs_list).items() if count > 1]
    
    #make a copy of the master workbook
    master_spreadsheet = 'Y:/spreadsheets/bdpl_master_spreadsheet.xlsx'
    master_copy = os.path.join('C:/temp', 'bdpl_master_copy.xlsx')
    
    if not os.path.exists('C:/temp'):
        os.mkdir('C:/temp')
    
    shutil.copy(master_spreadsheet, master_copy)
    
    #add all current barcodes into a list
    master_wb = openpyxl.load_workbook(master_copy)
    item_ws = master_wb['Item']

    master_list = []
    
    for barcode in item_ws['A'][1:]:
        if not barcode.value is None:
            master_list.append(barcode.value)
    
    already_used = [x for x in new_bcs_list if x in master_list]
    
    #note if any barcodes in the spreadsheet are duplicates
    if len(duplicate_barcodes) > 0:
        print('\n\nWARNING: spreadsheet includes duplicate barcode values:')
        for dup in duplicate_barcodes:
            print('\t%s\tRow: %s' % (dup, new_bcs[dup]))
    
    #note if any barcodes are already in the SDA are duplicated
    if len(already_used) > 0:
        print('\n\nWARNING: spreadsheet includes barcodes that have already been deposited to the SDA:')
        for dup in already_used:
            print('\t%s\tRow: %s' % (dup, new_bcs[dup]))

if __name__ == '__main__':

    os.system('cls')
    
    #print BDPL screen
    fname = "C:/BDPL/scripts/bdpl.txt"
    if os.path.exists(fname):
        with open(fname, 'r') as fin:
            print(fin.read())

    main()