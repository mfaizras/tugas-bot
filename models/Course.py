from models.TugasModel import TugasDataHandler
class Course:
    def __init__(self, course: dict):
        self.title:str = course['title']
        self.course_id:str = course['course-id']
        self.event_id:str = course['event-id']
        self.data:list['DataPerCourse'] = []
        for data in course['data']:
            self.data.append(
                DataPerCourse(data)
            )
    def to_dict(self) -> dict:
        course_dict = {
            'title': self.title,
            'course-id': self.course_id,
            'event-id': self.event_id,
            'data': [data.to_dict() for data in self.data]
        }
        return course_dict
    
    def detail_course(self):
        detail = {}
        detail['course'] = self.data[3].text if self.data[2].title == "Description" else self.data[2].text
        detail['description'] = self.data[2].text if self.data[2].title == "Description" else ""
        detail['deadline'] = self.data[0].text
        detail['assign_url'] = self.data[3].link if self.data[2].title == "Description" else self.data[2].link
        return DetailCourse(detail)
    
    def tugas_data_handler(self,source='MODDLE')-> TugasDataHandler:
        return TugasDataHandler((None,int(self.event_id),source,self.title,self.detail_course().course_title,self.detail_course().description,self.detail_course().deadline,self.detail_course().assign_url))

class DetailCourse:
    def __init__(self, data) -> None:
        self.course_title:str = data['course']
        self.deadline:str = data['deadline']
        self.description:str = data['description']
        self.assign_url:str = data['assign_url']
    

class DataPerCourse:
    def __init__(self, data:dict):
        self.title:str = data['title']
        self.text:str = data['text']
        self.link:str = data['link']
        
    def to_dict(self) -> dict:
        data_dict = {
            'title': self.title,
            'text': self.text,
            'link': self.link
        }
        return data_dict