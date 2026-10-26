from people import AnketaError, parse_line

class Registry:
    def __init__(self):
        self.accepted = []
        self.rejected = []

    def add(self, person):
        self.accepted.append(person)

    def load(self, filename):
        try:
            with open(filename, encoding="utf-8") as f:
                lines = f.read().splitlines()
        except FileNotFoundError:
            return False

        for num, line in enumerate(lines, 1):
            if not line.strip():
                continue
            try:
                person = parse_line(line)
                self.add(person)
            except AnketaError as e:
                self.rejected.append((num, line, str(e)))
        return True

    def __len__(self):
        return len(self.accepted)

    def stats_by_roles(self):
        result = {}
        for p in self.accepted:
            result[p.role()] = result.get(p.role(), 0) + 1
        return result

    def stats_by_groups(self):
        result = {}
        for p in self.accepted:
            group = p.group_for_stats()
            if group is not None:
                result[group] = result.get(group, 0) + 1
        return result

    def save(self, ok_file="ok.txt", err_file="errors.txt"):
        with open(ok_file, "w", encoding="utf-8") as f:
            for p in sorted(self.accepted):
                f.write(p.to_line() + "\n")

        with open(err_file, "w", encoding="utf-8") as f:
            for num, line, reason in self.rejected:
                f.write(f"строка {num}: {reason} | {line}\n")