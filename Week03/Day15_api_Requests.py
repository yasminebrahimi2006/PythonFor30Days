import requests
import json
from datetime import datetime


# ============================================================
# ۱. GET ساده - دریافت اطلاعات
# ============================================================
def get_github_user(username):
    """دریافت اطلاعات یه کاربر گیت‌هاب"""
    url = f"https://api.github.com/users/{username}"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "name": data.get("name"),
                "bio": data.get("bio"),
                "public_repos": data.get("public_repos"),
                "followers": data.get("followers"),
                "following": data.get("following"),
                "created_at": data.get("created_at"),
            }
        elif response.status_code == 404:
            return {"error": "User not found"}
        else:
            return {"error": f"Status code: {response.status_code}"}
    except requests.exceptions.Timeout:
        return {"error": "Request timed out"}
    except requests.exceptions.ConnectionError:
        return {"error": "No internet connection"}
    except Exception as e:
        return {"error": str(e)}


# ============================================================
# ۲. GET با پارامتر - جستجو
# ============================================================
def search_github_repos(query, limit=5):
    """جستجوی ریپوها توی گیت‌هاب"""
    url = "https://api.github.com/search/repositories"
    params = {
        "q": query,
        "sort": "stars",
        "order": "desc",
        "per_page": limit,
    }
    try:
        response = requests.get(url, params=params, timeout=10)
        if response.status_code == 200:
            data = response.json()
            repos = []
            for item in data.get("items", []):
                repos.append({
                    "name": item["name"],
                    "stars": item["stargazers_count"],
                    "url": item["html_url"],
                    "language": item.get("language"),
                })
            return repos
        return []
    except Exception as e:
        print(f"Error: {e}")
        return []


# ============================================================
# ۳. دریافت وضعیت آب و هوا (بدون API Key)
# ============================================================
def get_weather(city):
    """دریافت آب و هوای یه شهر با wttr.in"""
    url = f"https://wttr.in/{city}?format=j1"
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            current = data["current_condition"][0]
            return {
                "city": city,
                "temp_c": current["temp_C"],
                "feels_like": current["FeelsLikeC"],
                "humidity": current["humidity"],
                "description": current["weatherDesc"][0]["value"],
                "wind_kmph": current["windspeedKmph"],
            }
        return {"error": "City not found"}
    except Exception as e:
        return {"error": str(e)}


# ============================================================
# ۴. POST - ارسال داده
# ============================================================
def post_example():
    """مثال POST به httpbin.org"""
    url = "https://httpbin.org/post"
    payload = {
        "name": "Yasmin",
        "message": "Hello from Python!",
        "timestamp": datetime.now().isoformat(),
    }
    try:
        response = requests.post(url, json=payload, timeout=10)
        if response.status_code == 200:
            return response.json()
        return {"error": f"Status: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}


# ============================================================
# ۵. بررسی وضعیت یه سایت
# ============================================================
def check_site_status(url):
    """چک کردن وضعیت یه سایت"""
    try:
        response = requests.get(url, timeout=10)
        return {
            "url": url,
            "status_code": response.status_code,
            "is_up": response.status_code < 400,
            "response_time_ms": round(response.elapsed.total_seconds() * 1000, 2),
            "server": response.headers.get("Server", "Unknown"),
        }
    except requests.exceptions.ConnectionError:
        return {"url": url, "error": "Connection failed"}
    except requests.exceptions.Timeout:
        return {"url": url, "error": "Timeout"}
    except Exception as e:
        return {"url": url, "error": str(e)}


# ============================================================
# منوی اصلی
# ============================================================
def main():
    print("=" * 50)
    print("🌐 API Explorer")
    print("=" * 50)

    while True:
        print("\nOptions:")
        print("1. GitHub user info")
        print("2. Search GitHub repos")
        print("3. Weather")
        print("4. POST example")
        print("5. Check site status")
        print("6. Exit")

        choice = input("\nChoose (1-6): ").strip()

        if choice == "1":
            username = input("GitHub username: ").strip()
            result = get_github_user(username)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "2":
            query = input("Search query: ").strip()
            repos = search_github_repos(query)
            for repo in repos:
                print(f"⭐ {repo['stars']:>6} | {repo['name']} ({repo['language']})")
                print(f"         {repo['url']}")

        elif choice == "3":
            city = input("City: ").strip()
            result = get_weather(city)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "4":
            result = post_example()
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "5":
            url = input("URL (e.g., https://google.com): ").strip()
            result = check_site_status(url)
            print(json.dumps(result, indent=2, ensure_ascii=False))

        elif choice == "6":
            print("Bye! 👋")
            break

        else:
            print("Invalid choice!")


if __name__ == "__main__":
    main()