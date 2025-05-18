import datetime
import time
import threading

class StudyTask:
    def __init__(self, subject, start_time, end_time):
        self.subject = subject
        self.start_time = start_time
        self.end_time = end_time
        self.is_completed = False
        self.start_notified = False
        self.end_notified = False

    def check_and_notify(self):
        now = datetime.datetime.now()
        if self.is_completed:
            return

        # 시작 알림
        if not self.start_notified and abs((now - self.start_time).total_seconds()) <= 1:
            self.start_notified = True
            print(f"\n🔔 [알림] 📚 '{self.subject}' 공부 시작 시간입니다! ({now.strftime('%H:%M:%S')})")

        # 종료 알림
        if not self.end_notified and abs((now - self.end_time).total_seconds()) <= 1:
            self.end_notified = True
            print(f"\n🔔 [알림] 📕 '{self.subject}' 공부 종료 시간입니다! ({now.strftime('%H:%M:%S')})")

    def complete(self):
        self.is_completed = True
        print(f"✅ '{self.subject}' 공부를 완료했습니다.")

def get_tasks_from_user():
    tasks = []
    print("공부 일정을 등록하세요 (최대 5개, 종료하려면 Enter).")

    for _ in range(5):
        subject = input("\n과목 이름 (종료하려면 Enter): ").strip()
        if subject == "":
            break

        start_input = input("공부 시작 시간 (예: 2025-05-18 14:00): ")
        end_input = input("공부 종료 시간 (예: 2025-05-18 15:30): ")

        try:
            start_time = datetime.datetime.strptime(start_input, "%Y-%m-%d %H:%M")
            end_time = datetime.datetime.strptime(end_input, "%Y-%m-%d %H:%M")

            if start_time >= end_time:
                print("❌ 시작 시간은 종료 시간보다 빨라야 합니다.")
                continue

            tasks.append(StudyTask(subject, start_time, end_time))
        except ValueError:
            print("❌ 날짜 형식이 잘못되었습니다. 다시 입력하세요.")

    return tasks

def start_notification_loop(tasks):
    def loop():
        while any(not t.is_completed or not t.end_notified for t in tasks):
            for task in tasks:
                task.check_and_notify()
            time.sleep(1)
    thread = threading.Thread(target=loop, daemon=True)
    thread.start()

def print_menu(tasks):
    print("\n===== 공부 완료 메뉴 =====")
    print("0. 아무것도 완료하지 않음")
    for i, task in enumerate(tasks):
        status = "✅ 완료됨" if task.is_completed else "🕒 진행중"
        print(f"{i + 1}. {task.subject} [{status}]")
    choice = input("완료한 과목 번호를 입력하세요: ").strip()
    if choice.isdigit():
        idx = int(choice)
        if idx == 0:
            print("⏭️ 완료한 과목 없음")
        elif 1 <= idx <= len(tasks):
            task = tasks[idx - 1]
            if not task.is_completed:
                task.complete()
            else:
                print("⚠️ 이미 완료된 과제입니다.")
        else:
            print("⚠️ 올바르지 않은 번호입니다.")
    else:
        print("⚠️ 숫자로 입력해주세요.")

def main():
    tasks = get_tasks_from_user()
    if not tasks:
        print("⛔ 등록된 공부 일정이 없습니다.")
        return

    print("\n⏳ 공부 스케줄러 작동 중! (시작/종료 시각에 맞춰 콘솔에 알림 출력)")
    start_notification_loop(tasks)

    try:
        while any(not t.is_completed or not t.end_notified for t in tasks):
            time.sleep(5)
            print_menu(tasks)
    except KeyboardInterrupt:
        print("\n🔚 강제 종료됨")

    print("\n📋 공부 완료 현황:")
    for task in tasks:
        status = "✅ 완료" if task.is_completed else "❌ 미완료"
        print(f"{task.subject}: {status}")

if __name__ == "__main__":
    main()