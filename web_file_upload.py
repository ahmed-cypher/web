#!/usr/bin/env python3

import requests
import os
import sys
import time
from urllib.parse import urlparse

# ============================
# COLORS
# ============================
RED     = "\033[41m"
GREEN   = "\033[92m"
YELLOW  = "\033[93m"
BLUE    = "\033[34m"
PURPLE  = "\033[95m"
CYAN    = "\033[96m"
WHITE   = "\033[97m"
BOLD    = "\033[1m"
RESET   = "\033[0m"


class VulnerabilityTester:
    def __init__(self):#  
        self.vulnerable_sites = []
        self.tested_sites = 0
        
    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_banner(self):
        banner ="""\033[33m

███████╗██╗░░██╗██████╗░██╗░░░░░░█████╗░██╗████████╗
██╔════╝╚██╗██╔╝██╔══██╗██║░░░░░██╔══██╗██║╚══██╔══╝
█████╗░░░╚███╔╝░██████╔╝██║░░░░░██║░░██║██║░░░██║░░░
██╔══╝░░░██╔██╗░██╔═══╝░██║░░░░░██║░░██║██║░░░██║░░░
███████╗██╔╝╚██╗██║░░░░░███████╗╚█████╔╝██║░░░██║░░░
╚══════╝╚═╝░░╚═╝╚═╝░░░░░╚══════╝░╚════╝░╚═╝░░░╚═╝░░░
\033[37m"""
        print(banner)
    
    def validate_url(self, url):
        """التحقق من صحة وعنوان URL"""
        parsed = urlparse(url)
        if not parsed.scheme:
            url = 'http://' + url
        return url.rstrip('/')
    
    def test_site(self, site_url, file_path, file_content):
        """اختبار موقع واحد"""
        self.tested_sites += 1
        target_url = f"{site_url}/{file_path}"
        
        try:
            headers = {
                'User-Agent': 'Security-Test-Tool/1.0',
                'Content-Type': 'application/octet-stream'
            }
            
            response = requests.put(
                target_url,
                data=file_content,
                headers=headers,
                timeout=15,
                allow_redirects=False
            )
            
            # التحقق من الأكواد التي تشير إلى نجاح الرفع
            if response.status_code in [200, 201, 204]:
                return True, response.status_code
            else:
                return False, response.status_code
                
        except requests.exceptions.RequestException as e:
            return None, str(e)
    
    def run_test(self, sites_list, test_file):
        """تشغيل الاختبار على جميع المواقع"""
        # قراءة ملف الاختبار
        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                file_content = f.read()
            file_name = os.path.basename(test_file)
        except Exception as e:
            print(f"خطأ في قراءة الملف: {e}")
            return
        
        # قراءة قائمة المواقع
        try:
            with open(sites_list, 'r', encoding='utf-8') as f:
                sites = [line.strip() for line in f if line.strip()]
        except Exception as e:
            print(f"خطأ في قراءة القائمة: {e}")
            return
        
        print(f"\nبدء اختبار {len(sites)} موقع...")
        print("-" * 60)
        
        for i, site in enumerate(sites, 1):
            site = self.validate_url(site)
            print(f"[{i}/{len(sites)}] اختبار: {site}")
            
            is_vulnerable, status = self.test_site(site, file_name, file_content)
            
            if is_vulnerable:
                print(f"   ✓ ضعيف (كود: {status})")
                self.vulnerable_sites.append(f"{site}/{file_name}")
            elif is_vulnerable is False:
                print(f"   ✗ غير ضعيف (كود: {status})")
            else:
                print(f"   ! خطأ: {status}")
            
            # تأخير بين الطلبات لتجنب الحظر
            time.sleep(0.5)
    
    def save_results(self):
        """حفظ النتائج في ملف"""
        if not self.vulnerable_sites:
            print("\nلم يتم العثور على مواقع ضعيفة.")
            return
        
        with open('vulnerable_sites.txt', 'w', encoding='utf-8') as f:
            for site in self.vulnerable_sites:
                f.write(site + '\n')
        
        print(f"\nتم حفظ {len(self.vulnerable_sites)} موقع ضعيف في 'vulnerable_sites.txt'")
    
    def show_report(self):
        """عرض تقرير النتائج"""
        print("\n" + "="*60)
        print("تقرير النتائج النهائي:")
        print("="*60)
        print(f"عدد المواقع المختبرة: {self.tested_sites}")
        print(f"عدد المواقع الضعيفة: {len(self.vulnerable_sites)}")
        
        if self.tested_sites > 0:
            percentage = (len(self.vulnerable_sites) / self.tested_sites) * 100
            print(f"نسبة المواقع الضعيفة: {percentage:.2f}%")
        
        print("="*60)

def main():
    tester = VulnerabilityTester()
    tester.clear_screen()
    tester.show_banner()
    
 
    print("\n" +BLUE+ "="*60 +RESET)
    print(RED +BOLD +"مطور الأداة:أحمد عبدالمغني وفريقه"+RESET)
    print(BLUE+"="*60+RESET)
    
    

    
    
    try:
        # الحصول على المدخلات
        sites_file = input("\nأدخل مسار ملف قائمة المواقع: ").strip()
        test_file = input("أدخل مسار ملف الاختبار: ").strip()
        
        # التحقق من وجود الملفات
        if not os.path.exists(sites_file):
            print(f"خطأ: ملف '{sites_file}' غير موجود!")
            return
        
        if not os.path.exists(test_file):
            print(f"خطأ: ملف '{test_file}' غير موجود!")
            return
        
        # بدء الاختبار
        tester.run_test(sites_file, test_file)
        
        # حفظ النتائج وعرض التقرير
        tester.save_results()
        tester.show_report()
        
    except KeyboardInterrupt:
        print("\n\nتم إيقاف الأداة بواسطة المستخدم.")
    except Exception as e:
        print(f"\nحدث خطأ غير متوقع: {e}")

if __name__ == "__main__":
    main()
