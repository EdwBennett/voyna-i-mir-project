from pathlib import Path
import json


def load_users(path = "users.json"):
    if Path(path).exists():
     text=Path(path).read_text()
     return json.loads(text)
    else:
            return [{"name":"Ada","role":"admin"},{"name":"Grace","role":"editor"}]


def summarize_users(users):
      summary = []
      for user in users:
            summary.append({"name":user["name"],"label":f'{user["name"]} ({user["role"]})'})
      return summary


def print_summary(summary):
  for item in summary:
        print( item["label"] )


if __name__ == "__main__":
      users=load_users()
      summary=summarize_users(users)
      print_summary(summary)
      