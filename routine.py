class Rtn:
    def __init__(self):
        self.stage = 'first'
        self.count = 0
        self.status = 'stay'

    def run(self, total_status):
        if total_status == None:
            return 0, 0, self.status
        
        if total_status == 'rtn':
            print("rtn_stage:",self.stage)
            if self.stage == 'first':
                self.count += 1
                self.status = 'on'
                if self.count == 40:
                    self.count = 0
                    self.stage = 'second'
                return 0, 0.75, self.status
                #return 0, 0.82, self.status
            if self.stage == 'second':
                self.count += 1
                self.status = 'on'
                if self.count == 60:
                    self.count = 0
                    self.stage = 'third'
                return 0.6, 0.75, self.status
                #return 0.6, 0.82, self.status
            if self.stage == 'third':
                self.status = 'finish'
                return None, None, self.status
                
        
        return 0, 0, self.status