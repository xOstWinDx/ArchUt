import customtkinter


class owerclass(customtkinter.CTk):
    def __init__(self):
        super().__init__()


rt = owerclass()
rt.geometry('400x200')

rt.attributes('-topmost', True)
rt.attributes('state', 'DISABLED')
rt.mainloop()
