from pathlib import Path

from registry import Registry

BASE_DIR = Path(__file__).resolve().parent

def main():
    registry = Registry()

    if not registry.load(BASE_DIR / "anketa.txt"):
        print("Файл anketa.txt не найден")
        return

    print(f"{'№':>3}  {'ФИО':<30}{'Роль':<16}{'Группа/кафедра':<20}{'Телефон'}")
    print("-" * 95)

    for i, p in enumerate(sorted(registry.accepted), 1):
        print(
            f"{i:>3}  {p.fio:<30}{p.role():<16}"
            f"{p.extra():<20}{p.masked_phone()}"
        )

    print("-" * 95)
    print("Отклонено строк:", len(registry.rejected))
    for num, line, reason in registry.rejected:
        print(f"  строка {num}: {reason}")
        print(f"      {line}")

    print()
    print(f"Принято: {len(registry)} | Отклонено: {len(registry.rejected)}")

    print("По ролям:")
    for role, count in sorted(registry.stats_by_roles().items()):
        print(f"  {role}: {count}")

    print("По группам:")
    for group, count in sorted(registry.stats_by_groups().items()):
        print(f"  {group}: {count}")

    registry.save()
    print("Сохранено: ok.txt и errors.txt")

if __name__ == "__main__":
    main()