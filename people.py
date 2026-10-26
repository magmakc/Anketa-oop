class AnketaError(Exception):
    pass

class Person:
    type_code = "?"

    def __init__(self, fio, mail, phone):
        self.fio = self.check_fio(fio)
        self.mail = self.check_mail(mail)
        self.phone = self.check_phone(phone)

    @staticmethod
    def check_fio(text):
        parts = text.split()
        if len(parts) < 2:
            raise AnketaError("в ФИО меньше двух слов")
        return " ".join(parts).title()

    @staticmethod
    def check_mail(text):
        mail = text.strip().lower()
        if mail.count("@") != 1:
            raise AnketaError(f"почта неверная: {mail}")
        name, domain = mail.split("@")
        if not name or not domain:
            raise AnketaError(f"почта неверная: {mail}")
        if "." not in domain or domain.startswith(".") or domain.endswith("."):
            raise AnketaError(f"почта неверная: {mail}")
        return mail

    @staticmethod
    def check_phone(text):
        digits = "".join(ch for ch in text if ch.isdigit())
        if len(digits) != 11:
            raise AnketaError(f"в телефоне {len(digits)} цифр вместо 11")
        if digits[0] not in "78":
            raise AnketaError("телефон должен начинаться с 7 или 8")
        return f"+7 ({digits[1:4]}) {digits[4:7]}-{digits[7:9]}-{digits[9:]}"

    def masked_phone(self):
        return self.phone[:9] + "***-**-" + self.phone[-2:]

    def short_fio(self):
        parts = self.fio.split()
        if len(parts) >= 3:
            return f"{parts[0]} {parts[1][0]}. {parts[2][0]}."
        if len(parts) == 2:
            return f"{parts[0]} {parts[1][0]}."
        return self.fio

    def role(self):
        return "—"

    def extra(self):
        return ""

    def group_for_stats(self):
        return None

    def to_line(self):
        return f"{self.type_code};{self.fio};{self.mail};{self.phone};{self.extra()}"

    def __str__(self):
        return f"{self.fio} ({self.role()}), {self.extra()}, {self.masked_phone()}"

    def __lt__(self, other):
        return self.fio < other.fio

class Student(Person):
    type_code = "s"

    def __init__(self, fio, mail, phone, group):
        super().__init__(fio, mail, phone)
        self.group = self.check_group(group)

    @staticmethod
    def check_group(text):
        group = text.strip().lower()
        if not group:
            raise AnketaError("группа не указана")
        return group

    def role(self):
        return "студент"

    def extra(self):
        return self.group

    def group_for_stats(self):
        return self.group

class Teacher(Person):
    type_code = "t"

    def __init__(self, fio, mail, phone, department):
        super().__init__(fio, mail, phone)
        self.department = self.check_department(department)

    @staticmethod
    def check_department(text):
        department = text.strip()
        if not department:
            raise AnketaError("кафедра не указана")
        return department

    def role(self):
        return "преподаватель"

    def extra(self):
        return self.department

def parse_line(line):
    fields = [f.strip() for f in line.split(";")]
    if len(fields) != 5:
        raise AnketaError(f"полей {len(fields)} вместо 5")

    type_code, fio, mail, phone, extra = fields
    type_code = type_code.lower()

    if type_code == "s":
        return Student(fio, mail, phone, extra)
    if type_code == "t":
        return Teacher(fio, mail, phone, extra)

    raise AnketaError(f"неизвестный тип: {type_code}")