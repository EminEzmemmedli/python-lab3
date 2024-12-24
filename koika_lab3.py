from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
import os
import time

# .env faylını yükləyin
load_dotenv()

# .env faylından istifadəçi adı və şifrəni oxuyun
username = os.getenv('KOICA_USERNAME')
password = os.getenv('KOICA_PASSWORD')

# ChromeDriver yüklənir
driver = webdriver.Chrome()

# Saytı açır
driver.get("https://sso.aztu.edu.az")  # URL-ni buraya əlavə edin

try:
    # Sayfanın tam yükləndiyini gözləyirik
    WebDriverWait(driver, 20).until(
        lambda driver: driver.execute_script("return document.readyState == 'complete'")
    )

    # İstifadəçi adı və şifrə daxil edilir
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "Username"))
    )
    username_input.send_keys(username)  # İstifadəçi adı .env faylından alınır

    password_input = driver.find_element(By.ID, "Password")
    password_input.send_keys(password)  # Şifrə .env faylından alınır

    # Daxil ol düyməsi basılır
    submit_button = driver.find_element(By.XPATH, "//button[@type='submit']")
    submit_button.click()

    # Tələbə keçidinə basır
    student_link = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Tələbə keçid"))
    )
    student_link.click()

    # Fənlər linkini tapmaq üçün səhifənin yüklənməsini gözləyirik
    WebDriverWait(driver, 20).until(
        lambda driver: driver.execute_script("return document.readyState == 'complete'")
    )

    # Fənlər bölməsini tapırıq
    courses_section = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.XPATH, "//span[contains(text(),'Fənlər')]/parent::a"))
    )
    courses_section.click()

    # Python proqramlaşdırma dili linkini tapırıq
    python_course = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Python proqramlaşdırma dili"))
    )
    python_course.click()

    # Davamiyyət bölməsini tapırıq
    attendance_tab = WebDriverWait(driver, 20).until(
        EC.element_to_be_clickable((By.LINK_TEXT, "Davamiyyət"))
    )

    # JavaScript ilə klikləmə
    driver.execute_script("arguments[0].click();", attendance_tab)

    # Davamiyyət cədvəlini tapırıq
    attendance_table = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, "//table"))
    )

    # Cədvəl məlumatlarını fayla yazırıq
    with open("attendance_data.csv", "w", encoding="utf-8") as file:
        # Sətirləri tapırıq
        rows = attendance_table.find_elements(By.TAG_NAME, "tr")
        if not rows:  # Əgər cədvəl boşdursa
            print("Cədvəl boşdur və ya satırlar tapılmadı.")
            with open("attendance_data.txt", "w", encoding="utf-8") as file:
                file.write("Cədvəl boşdur.\n")
        else:
            # Başlıq sətiri üçün
            headers = rows[0].find_elements(By.TAG_NAME, "th")
            with open("attendance_data.txt", "w", encoding="utf-8") as file:
                file.write(",".join([header.text.strip() for header in headers]) + "\n")

        # Qalan məlumatları yazırıq
        for row in rows[1:]:
            columns = row.find_elements(By.TAG_NAME, "td")
            file.write(",".join([col.text.strip() for col in columns]) + "\n")

    print("Davamiyyət məlumatları 'attendance_data.csv' faylına yazıldı.")

finally:
    driver.quit()
