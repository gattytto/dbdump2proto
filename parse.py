#!/usr/bin/python3
import sys,getopt,struct,os,string

def SwitchFieldTypes(argument):
    switcher = {
        "C": "This is Case String ",
        "N": "This is Case Number ",
        "D": "This is Case Timestamp ",
    }
    return switcher.get(argument)


def main(argv):
	
	inputfile = ""
	outputfile = ""

	for arg in argv:
		arch=""
		print("arg: ", arg)

		if not os.path.isfile(arg):
			print("not a file")
			sys.exit(2)

		try:
			arch=open(arg,"rb")
		except:
			print("some error with file")
			sys.exit(2)

		#parse first 32 bytes for magic number and file info
		header = arch.read(4)
		if header.hex() != "03780504":
			print("invalid magic number")
			sys.exit(2)
		recordcount = arch.read(4)
		firstrecordoffset = arch.read(2)
		recordsize = arch.read(2)
		nada=arch.read(20)
		firstrecordint = struct.unpack("<H",firstrecordoffset)[0]
		fieldscount = int(((firstrecordint-1)/32)-1)
		print("header: ",header.hex())
		print("recordcount: ", int.from_bytes(recordcount,"little") )
		print("first record offset: ", hex(struct.unpack("<H",firstrecordoffset)[0]))
		print("record size: ", hex(struct.unpack("<H",recordsize)[0]))
		print("fields: ", fieldscount, "\n")
		filenamewithoutext = arg.split(".")[0]
		fileproto=""
		
		try:
			fileproto = open(filenamewithoutext+".proto","w")
		except:
			print("cant open output proto file")
			arch.close()
			sys.exit(2)

		fileproto.write("message " + filenamewithoutext.capitalize() + " { \n")

		for x in range(fieldscount):
			print("number: ", x)
			fieldname=arch.read(11)
			fieldtype=arch.read(1)
			nada=arch.read(4)
			fieldsize=arch.read(1)
			fieldintdecimals=arch.read(1)
			nada=arch.read(14)
			print("field name: ", fieldname.decode("UTF-8"))
			print("field type: ", SwitchFieldTypes(fieldtype.decode("UTF-8")))
			print("field size: ", int.from_bytes(fieldsize,"little"))
			print("decimal digits: ", int.from_bytes(fieldintdecimals,"little"), "\n")

			#generate protos
			if fieldtype.decode("UTF-8") == "C":
				fileproto.write("    string " + fieldname.decode("UTF-8").lower() + " = " + str(x) + "; \n")
			


		fileproto.write("} \n")
		fileproto.close()
		arch.close()

	print("will be ", filenamewithoutext+".proto")
	input("done")




if __name__ == "__main__":
   main(sys.argv[1:])