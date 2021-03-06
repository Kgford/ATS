#import cv2
import barcode #https://pypi.org/project/python-barcode/
#from pyzbar import pyzbar #https://towardsdatascience.com/building-a-barcode-qr-code-reader-using-python-360e22dfb6e5
from barcode.writer import ImageWriter
from io import BytesIO
from django.core.files import File

class Barcode:
    def __init__ (self, part_num,file_path,standard,test):
        self.part_num = part_num
        self.file_path = file_path
        self.standard = standard
        self.test = test
        print('part_num =',self.part_num)
        print('file_path =',self.file_path)
        print('standard =',self.standard)
        
    '''
    def read_barcodes(self):
        #1
        camera = cv2.VideoCapture(0)
        ret, frame = camera.read()
        #2
        while ret:
            ret, frame = camera.read()
            frame = self.decode_barcodes(frame)
            cv2.imshow('Barcode/QR code reader', frame)
            if cv2.waitKey(1) & 0xFF == 27:
                break
        #3
        camera.release()
        cv2.destroyAllWindows()
    #4
    if __name__ == '__main__':
        main()


    def decode_barcodes(self,frame):
        barcodes = pyzbar.decode(frame)
        print('barcodes=',barcodes)
        for barcode in barcodes:
            x, y , w, h = barcode.rect
            #1
            barcode_info = barcode.data.decode('utf-8')
            print('barcode_info=',barcode_info)
            cv2.rectangle(frame, (x, y),(x+w, y+h), (0, 255, 0), 2)
            
            #2
            font = cv2.FONT_HERSHEY_DUPLEX
            cv2.putText(frame, barcode_info, (x + 6, y - 6), font, 2.0, (255, 255, 255), 1)
            #3
            with open("barcode_result.txt", mode ='w') as file:
                file.write("Recognized Barcode:" + barcode_info)
        return frame
    '''
    def create_barcode_svg(self):
        # class and pass the number 
        if self.standard =='code39':
             CODE39 = barcode.get_barcode_class('code39')
             my_code = CODE39(str(self.part_num))
        elif self.standard =='code128':
             CODE128 = barcode.get_barcode_class('code128')
             my_code = CODE128(str(self.part_num))
        elif self.standard =='ean':
             EAN = barcode.get_barcode_class('ean')    
             my_code = EAN(str(self.part_num))
        elif self.standard =='ean13':
             EAN13 = barcode.get_barcode_class('ean13')       
             my_code = EAN13(str(self.part_num))
        elif self.standard =='ean8':
             EAN8 = barcode.get_barcode_class('ean8') 
             my_code = EAN8(str(self.part_num))
        elif self.standard =='gs1':
             GS1 = barcode.get_barcode_class('gs1')    
             my_code = GS1(str(self.part_num))
        elif self.standard =='gtin':
             GTIN = barcode.get_barcode_class('gtin')  
             my_code = GITN(str(self.part_num))
        elif self.standard =='isbn':
             ISBN = barcode.get_barcode_class('isbn')  
             my_code = ISBN(str(self.part_num))
        elif self.standard =='isbn10':
             ISBN10 = barcode.get_barcode_class('isbn10')
             my_code = ISBN10(str(self.part_num))
        elif self.standard =='isbn13':
             ISBN13 = barcode.get_barcode_class('isbn13')
             my_code = ISBN13(str(self.part_num))
        elif self.standard =='issn':
             ISSN= barcode.get_barcode_class('issn')
             my_code = ISSN(str(self.part_num))
        elif self.standard =='jan':
             JAN = barcode.get_barcode_class('jan')
             my_code = JAN(str(self.part_num))
        elif self.standard =='pzn':
             PZN = barcode.get_barcode_class('pzn')
             my_code = PZN(str(self.part_num))
        elif self.standard =='upc':
             UPC = barcode.get_barcode_class('upc')
             my_code = UPC(str(self.part_num))
        elif self.standard =='upcn':
             UPCN = barcode.get_barcode_class('upcn')
             my_code = UPCN(str(self.part_num))

        # Our barcode is ready. Let's save it. 
        my_code.save("new_code")
        
    def create_barcode_byte(self):
        # class and pass the number 
        rv = BytesIO()
        if self.standard =='code39':
             CODE39 = barcode.get_barcode_class('code39')
             my_code = CODE39(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='code128':
             CODE128 = barcode.get_barcode_class('code128')
             my_code = CODE128(str(self.part_num), writer=ImageWriter()).write(rv)
             print('COD128=',rv.getvalue())
        elif self.standard =='ean':
             EAN = barcode.get_barcode_class('ean')    
             my_code = EAN(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='ean13':
             EAN13 = barcode.get_barcode_class('ean13')       
             my_code = EAN13(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='ean8':
             EAN8 = barcode.get_barcode_class('ean8') 
             my_code = EAN8(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='gs1':
             GS1 = barcode.get_barcode_class('gs1')    
             my_code = GS1(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='gtin':
             GTIN = barcode.get_barcode_class('gtin')  
             my_code = GTIN(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='isbn':
             ISBN = barcode.get_barcode_class('isbn')  
             my_code = ISBN(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='isbn10':
             ISBN10 = ISBN10.get_barcode_class('isbn10')
             my_code = COD128(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='isbn13':
             ISBN13 = barcode.get_barcode_class('isbn13')
             my_code = ISBN13(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='issn':
             ISSN = barcode.get_barcode_class('issn')
             my_code = ISSN(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='jan':
             JAN = barcode.get_barcode_class('jan')
             my_code = JAN(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='pzn':
             PZN = barcode.get_barcode_class('pzn')
             my_code = PZN(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='upc':
             UPC = barcode.get_barcode_class('upc')
             my_code = UPC(str(self.part_num), writer=ImageWriter()).write(rv)
        elif self.standard =='upcn':
             UPCN = barcode.get_barcode_class('upcn')
             my_code = UPCN(str(self.part_num), writer=ImageWriter()).write(rv)
        
        print('rv=',rv)
        return rv
          
        # Our barcode is ready. Let's save it. 
        my_code.save("new_code")
    
    def create_barcode_jpg(self):
        if self.standard =='code39':
             COD39 = barcode.get_barcode_class('code39')
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                CODE9(str(self.part_num), writer=ImageWriter()).write(f)  
        elif self.standard =='code128':
             COD128 = barcode.get_barcode_class('code128')
             print('in 128')
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                COD128(str(self.part_num), writer=ImageWriter()).write(f)
                print('COD128=',f)
        elif self.standard =='ean':
             EAN = barcode.get_barcode_class('ean')    
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                EAN(str(self.part_num), writer=ImageWriter()).write(f) 
                print('COD128=',f)
        elif self.standard =='ean13':
             EAN13 = barcode.get_barcode_class('ean13')       
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                EAN13(str(self.part_num), writer=ImageWriter()).write(f) 
        elif self.standard =='ean8':
             EAN8 = barcode.get_barcode_class('ean8') 
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                EAN8(str(self.part_num), writer=ImageWriter()).write(f) 
        elif self.standard =='gs1':
             GS1 = barcode.get_barcode_class('gs1')    
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                GS1(str(self.part_num), writer=ImageWriter()).write(f) 
        elif self.standard =='gtin':
             GTIN = barcode.get_barcode_class('gtin')  
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                GTIN(str(self.part_num), writer=ImageWriter()).write(f) 
                print('GTIN=',f)
        elif self.standard =='isbn':
             ISBN = barcode.get_barcode_class('isbn')  
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                ISBN(str(self.part_num), writer=ImageWriter()).write(f) 
        elif self.standard =='isbn10':
             ISBN10 = ISBN10.get_barcode_class('isbn10')
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                ISBN10(str(self.part_num), writer=ImageWriter()).write(f) 
        elif self.standard =='isbn13':
             ISBN13 = barcode.get_barcode_class('isbn13')
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                ISBN13(str(self.part_num), writer=ImageWriter()).write(f) 
                print('ISBN13=',f)
        elif self.standard =='issn':
             ISSN = barcode.get_barcode_class('issn')
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                ISSN(str(self.part_num), writer=ImageWriter()).write(f) 
                print('ISSN=',f)
        elif self.standard =='jan':
             JAN = barcode.get_barcode_class('jan')
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                JAN(str(self.part_num), writer=ImageWriter()).write(f) 
        elif self.standard =='pzn':
             PZN = barcode.get_barcode_class('pzn')
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                PZN(str(self.part_num), writer=ImageWriter()).write(f) 
        elif self.standard =='upc':
             UPC = barcode.get_barcode_class('upc')
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                UPC(str(self.part_num), writer=ImageWriter()).write(f) 
        elif self.standard =='upcaa':
             UPCA = barcode.get_barcode_class('upca')
             with open(self.file_path + str(self.part_num) + '.jpg', 'wb') as f:
                UPCA(str(self.part_num), writer=ImageWriter()).write(f) 

        
    def create_barcode_png(self):
        # pass the number with the ImageWriter() as the  
        # writer
        if self.standard =='code39':
             CODE39 = barcode.get_barcode_class('code39')
             my_code = CODE39(str(self.part_num), writer=ImageWriter())
        elif self.standard =='code128':
             CODE128 = barcode.get_barcode_class('code128')
             my_code = COD128(str(self.part_num), writer=ImageWriter())
        elif self.standard =='ean':
             EAN = barcode.get_barcode_class('ean')    
             my_code = EAN(str(self.part_num), writer=ImageWriter())
        elif self.standard =='ean13':
             EAN13 = barcode.get_barcode_class('ean13')       
             my_code = EAN13(str(self.part_num), writer=ImageWriter())
        elif self.standard =='ean8':
             EAN8 = barcode.get_barcode_class('ean8') 
             my_code = EAN8(str(self.part_num), writer=ImageWriter())
        elif self.standard =='gs1':
             GS1 = barcode.get_barcode_class('gs1')    
             my_code = GS1(str(self.part_num), writer=ImageWriter())
        elif self.standard =='gtin':
             GTIN = barcode.get_barcode_class('gtin')  
             my_code = GTIN(str(self.part_num), writer=ImageWriter())
        elif self.standard =='isbn':
             ISBN = barcode.get_barcode_class('isbn')  
             my_code = ISBN(str(self.part_num), writer=ImageWriter())
        elif self.standard =='isbn10':
             ISBN10 = ISBN10.get_barcode_class('isbn10')
             my_code = COD128(str(self.part_num), writer=ImageWriter())
        elif self.standard =='isbn13':
             ISBN13 = barcode.get_barcode_class('isbn13')
             my_code = ISBN13(str(self.part_num), writer=ImageWriter())
        elif self.standard =='issn':
             ISSN = barcode.get_barcode_class('issn')
             my_code = ISSN(str(self.part_num), writer=ImageWriter())
        elif self.standard =='jan':
             JAN = barcode.get_barcode_class('jan')
             my_code = JAN(str(self.part_num), writer=ImageWriter())
        elif self.standard =='pzn':
             PZN = barcode.get_barcode_class('pzn')
             my_code = PZN(str(self.part_num), writer=ImageWriter())
        elif self.standard =='upc':
             UPC = barcode.get_barcode_class('upc')
             my_code = UPC(str(self.part_num), writer=ImageWriter())
        elif self.standard =='upcn':
             UPCN = barcode.get_barcode_class('upcn')
             my_code = UPCN(str(self.part_num), writer=ImageWriter())       
          
        # Our barcode is ready. Let's save it.
        print('save file = ',self.file_path + str(self.part_num))
        my_code.save(self.file_path + str(self.part_num))
        
        
        
        
        