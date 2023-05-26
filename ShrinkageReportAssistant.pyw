import babel.numbers
import os
from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from datetime import datetime
from shrinkageCalculator import shrinkageReport

class ShrinkageReportAssistant:
	def __init__(self, window):
		# Initializations 
		self.wind = window
		self.wind.title('Shrinkage Report Assistant')
		self.wind.geometry('542x515')
		self.wind.resizable(False, False)

		self.date_selected = False
		self.set_hps = False
		#self.profile = r"C:\Users\santi\AppData\Local\Google\Chrome\User Data\Default"
		with open('Profile.txt') as f:
			self.profile = f.readlines()[0]

		#-------------------------------------
		# Left column (messages, calendar and information)
		#-------------------------------------
		frame_column_1 = LabelFrame(self.wind, borderwidth = '0')
		frame_column_1.place(x=10, y=0, width=280, relheight=1)

		#-------------------------------------
		# Message frame
		#-------------------------------------
		frame_msg = LabelFrame(frame_column_1, text = 'Message')
		frame_msg.place(x=0, y=0, relwidth=.99, height=55)

		self.message = Label(frame_msg, text = 'No message')
		self.message.place(x = 10, y = 4)

		#-------------------------------------
		# Calendar
		#-------------------------------------
		frame_cal = LabelFrame(frame_column_1, text = 'Select date', borderwidth=2)
		frame_cal.place(x=0, y=55, relwidth=.99, height=260)

		# Current date for calendar default
		today = datetime.now()
		day = today.day
		month = today.month
		year = today.year

		self.calendar = Calendar(frame_cal, selectmode = 'day', year = year, month = month, day = day, date_pattern="y-mm-dd")
		self.calendar.place(x = 10, y = 5)

		Button(frame_cal, text = 'Select Date', relief="solid", fg='black', bg = '#D3D3D3', 
			font=("Arial",8,"bold"), bd = 1, width = 34, height = 2, command = self.get_date).place(x = 12, y = 195)

		#-------------------------------------
		# Information
		#-------------------------------------
		frame_info = LabelFrame(frame_column_1, text = 'Information', borderwidth=2)
		frame_info.place(x=0, y=315, relwidth=.99, height=74)

		Label(frame_info, text = '1. Select and save date to report shrinkage').place(x=5, y=4)
		Label(frame_info, text = '2. Add harvest performances for herbs and pots').place(x=5, y=24) 
		
		Button(frame_column_1, text = 'Upload to Farmboard', relief="solid", fg='black', bg = '#95CB78', font=("Arial",8,"bold"), bd = 1, width = 37, height = 2, command = lambda: self.upload_values()).place(x = 3, y = 465)

		#-------------------------------------
		# Setting Harvest Performances
		#-------------------------------------
		center_col_width = 240

		self.frame_hps = LabelFrame(self.wind, text = 'Harvest Performances [%]')
		self.frame_hps.place(x=294, y=0, width= center_col_width, height=510)

		self.col_width = 13
		self.headers_width = 7
		self.headers_height = 10
		self.col_height = 1
		self.herbs_col_start = 7
		self.pots_col_start = 97

		Label(self.frame_hps, text = 'Variety / HP [%]', width=self.col_width).place(x = self.herbs_col_start, y = 8+self.col_height)

		headers = ['Herbs', 'Pots']

		for i in range(len(headers)):
			Label(self.frame_hps, text = headers[i], bg='#CCCCCC', width= self.headers_width).place(x = (102+self.herbs_col_start)+62*i, y = self.headers_height)

		self.varieties = ['Italian Basil', 'Flat Coriander', 'Thyme', 'Peppermint', 'Rosemary', 'Flat Parsley', 'Curly Parsley', 'Sage', 'Dill', 'Chervil', 'Watercress', 'Melissa', 'Oregano', 'Pea Tops']

		Label(self.frame_hps, bg = '#EDEDED', width = self.col_width, height = 25).place(x = 5, y = 40 + self.col_height)

		for i in range(len(self.varieties)):
			Label(self.frame_hps, text = f'{self.varieties[i]}:', font = ('Roboto', 10, 'italic'), width=self.col_width-1, height = self.col_height).place(x = 5, y = 7+self.col_height+(i+1)*29)

		self.herb_x = 100 + self.herbs_col_start
		self.herb_y = self.col_height + 24
		self.entry_width = 15
		self.entry_height = 21

		self.frame_hps_values = LabelFrame(self.frame_hps, borderwidth=0)
		self.frame_hps_values.place(x = 105, y = 33)

		window.bind_all("<<Paste>>", self.paste)
		self.table = self.generate_columns(14,2)

		Button(self.frame_hps, text = 'Set HPs values', relief="solid", fg='black', bg = '#D3D3D3', font=("Arial",8,"bold"), bd = 1, width = 16, height = 2, command = lambda: self.save_values()).place(x = 107, y = 445)

	def generate_columns(self, rows, columns):
		self.table = []
		for r in range(rows):
			row = []
			for c in range(columns):
				var   = StringVar()
				entry = Entry(self.frame_hps_values, textvar=var, justify = CENTER, width = 7, font = ('Roboto', 11))
				entry.grid(row=r, column=c, pady=1, padx=1, ipady=3)
				row.append(var)
			self.table.append(row)
		return self.table

	def paste(self, event):
		rows = window.clipboard_get().split('\n')

		for r, row in enumerate(rows):
			values = row.split('\t')
			for c, value in enumerate(values):
				self.table[r][c].set(value)
		return self.table

	def save_values(self):
		self.hps_table = [[] for x in range(len(self.varieties))]

		if self.date_selected == True:

			try:

				for i in range(len(self.varieties)):
					if self.table[i][0].get() == '':
						self.hps_table[i].append(0)
					elif 0 <= int(self.table[i][0].get()) <= 100:
						self.hps_table[i].append(int(self.table[i][0].get()))
					else:
						self.message['text'] = "All inputs must be between 0 and 100%"
						self.message['fg'] = 'red'
						self.message['font'] = ('Helvetica', 8, 'bold')
						self.set_hps = False

					if self.table[i][1].get() == '':
						self.hps_table[i].append(0)
					elif 0 <= int(self.table[i][1].get()) and int(self.table[i][1].get()) <= 100:
						self.hps_table[i].append(int(self.table[i][1].get()))

				self.set_hps = True
				self.message['text'] = f'Harvest Performances saved. Ready to upload'
				self.message['fg'] = 'green'
				self.message['font'] = ('Helvetica', 8, 'bold')

			except:
				self.message['text'] = "All inputs must be between 0 and 100%"
				self.message['fg'] = 'red'
				self.message['font'] = ('Helvetica', 8, 'bold')
				self.set_hps = False

		else:
			self.message['text'] = "Please, select date"
			self.message['fg'] = 'red'
			self.message['font'] = ('Helvetica', 8, 'bold')
			self.set_hps = False

	def upload_values(self):
		if self.date_selected == False:
			self.message['text'] = "Please, select date and set HPs"
			self.message['fg'] = 'red'
			self.message['font'] = ('Helvetica', 8, 'bold')

		elif self.set_hps == False:
			self.message['text'] = "Please, check and set inputs"
			self.message['fg'] = 'red'
			self.message['font'] = ('Helvetica', 8, 'bold')

		else:
			hps = {'Flat Parsley_2x18cc': self.hps_table[5][0], 'Curly Parsley_33cc_3weeks': self.hps_table[6][0], 'Thyme_33cc 3Week Acre': self.hps_table[2][0], 'Flat Coriander_33cc CPH': self.hps_table[1][0], 'Rosemary_33cc CPH': self.hps_table[4][0], 'Green Mint_33cc CPH': self.hps_table[3][0], 'Green Mint_33cc CPH': self.hps_table[3][0], 'Sage_33cc': self.hps_table[7][0], 'Italian Basil_33cc CPH': self.hps_table[0][0], 'Dill_33cc CPH': self.hps_table[8][0], 'Dill_33cc CPH': self.hps_table[8][0], 'Pots_Italian Basil_2x33cc CPH_Bs105': self.hps_table[0][1], 'Pots_Italian Basil_2x33cc CPH_Bs105': self.hps_table[0][1], 'Pots_Flat Coriander_2x33cc CPH': self.hps_table[1][1], 'Pots_Thyme_2x33cc CPH': self.hps_table[2][1], 'Pots_Green Mint_2x33cc CPH': self.hps_table[3][1], 'Pots_Green Mint_2x33cc CPH': self.hps_table[3][1], 'Pots_Rosemary_2x33cc CPH': self.hps_table[4][1], 'Pots_Chervil_2x33cc CPH': self.hps_table[9][1], 'Pots_Watercress_2x33cc CPH': self.hps_table[10][1], 'Pots_Melissa_2x33cc CPH': self.hps_table[11][1], 'Pots_Oregano_2x33cc': self.hps_table[12][1], 'Pots_Flat Parsley_2x33cc CPH': self.hps_table[5][1], 'Pea Tops - Early Harvest': self.hps_table[13][1], 'Caravel_33cc (3 Week Acre)': 100, 'Crystal_33cc (3 Week Acre)': 100, 'Red Oakleaf_ 33cc (3 week Acre)': 100, 'Red_romaine_33cc (3 Week Acre)': 100}

			shrinkageReport(self.profile, self.date, hps)

	def get_date(self):
		self.date = self.calendar.get_date()
		self.date_selected = True
		self.message['text'] = f'Date selected: {self.date}'
		self.message['fg'] = 'green'
		self.message['font'] = ('Helvetica', 8, 'bold')

if __name__ == '__main__':
	window = Tk()
	application = ShrinkageReportAssistant(window)
	window.mainloop()

