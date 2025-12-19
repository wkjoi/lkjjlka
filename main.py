import json
import random
import os
import time
from datetime import datetime, timedelta
from pathlib import Path
import requests

class MCQPostGenerator:
    def __init__(self, json_file='question_bank.json', page_id=None, access_token=None):
        self.json_file = json_file
        self.page_id = page_id
        self.access_token = access_token
        self.mcqs = self.load_questions()
        
    def load_questions(self):
        """Load MCQ questions from JSON file"""
        try:
            with open(self.json_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                return data.get('mcqs', [])
        except FileNotFoundError:
            print(f"Error: {self.json_file} not found!")
            return []
        except json.JSONDecodeError:
            print(f"Error: Invalid JSON in {self.json_file}")
            return []
    
    def get_questions_without_image(self, count=10):
        """Get random questions where imageUrl is empty"""
        questions_without_image = [q for q in self.mcqs if q.get('imageUrl', '') == '']
        
        if len(questions_without_image) < count:
            print(f"Warning: Only {len(questions_without_image)} questions available without images")
            return questions_without_image
        
        return random.sample(questions_without_image, count)
    
    def generate_post_header(self, question_count):
        """Generate post header with date"""
        bengali_months = {
            1: 'জানুয়ারি', 2: 'ফেব্রুয়ারি', 3: 'মার্চ', 4: 'এপ্রিল',
            5: 'মে', 6: 'জুন', 7: 'জুলাই', 8: 'আগস্ট',
            9: 'সেপ্টেম্বর', 10: 'অক্টোবর', 11: 'নভেম্বর', 12: 'ডিসেম্বর'
        }
        
        today = datetime.now()
        bengali_date = f"{today.day} {bengali_months[today.month]} {today.year}"
        
        header = f"""আজের ICT MCQ Practice | {bengali_date}
📚 ICT Tutor Pro App থেকে বাছাইকৃত {question_count} টি গুরুত্বপূর্ণ প্রশ্ন
━━━━━━━━━━━━━━━━━━━━"""
        
        return header
    
    def generate_post_footer(self):
        """Generate post footer"""
        footer = """
━━━━━━━━━━━━━━━━━━━━
✅ সঠিক উত্তরগুলো চিহ্নিত করা আছে

📱 আরও MCQ Practice করতে ICT Tutor Pro App ডাউনলোড করুন:
https://play.google.com/store/apps/details...

#ICTTutorPro #HSC #Honours #MCQ #BoardExam"""
        
        return footer
    
    def post_type_1_with_answers(self, questions):
        """Post Type 1: Questions with answer key and marks"""
        post = self.generate_post_header(len(questions))
        post += "\n\n"
        
        for idx, q in enumerate(questions, 1):
            post += f"প্রশ্ন {idx}:\n"
            post += f"{q['question']}\n"
            
            for option in q['options']:
                # Highlight correct answer
                if option == q['answer']:
                    post += f"✅ {option}\n"
                else:
                    post += f"{option}\n"
            
            post += "\n"
        
        post += self.generate_post_footer()
        return post
    
    def post_type_2_questions_only(self, questions):
        """Post Type 2: Questions only, answers in comments"""
        # Main post - Questions only
        main_post = self.generate_post_header(len(questions))
        main_post += "\n\n"
        
        for idx, q in enumerate(questions, 1):
            main_post += f"প্রশ্ন {idx}:\n"
            main_post += f"{q['question']}\n"
            
            for option in q['options']:
                main_post += f"{option}\n"
            
            main_post += "\n"
        
        main_post += "\n💬 সঠিক উত্তরগুলো কমেন্টে দেওয়া হবে!"
        main_post += "\n📱 আরও MCQ Practice করতে ICT Tutor Pro App ডাউনলোড করুন:"
        main_post += "\nhttps://play.google.com/store/apps/details..."
        main_post += "\n\n#ICTTutorPro #HSC #Honours #MCQ #BoardExam"
        
        # Comment with answers
        comment = "✅ সঠিক উত্তরসমূহ:\n\n"
        for idx, q in enumerate(questions, 1):
            comment += f"প্রশ্ন {idx}: {q['answer']}\n"
        
        comment += "\n🎯 কতগুলো সঠিক হয়েছে? কমেন্টে জানান!"
        
        return main_post, comment
    
    def post_type_3_quiz_challenge(self, questions):
        """Post Type 3: Interactive Quiz Challenge with scoring"""
        bengali_months = {
            1: 'জানুয়ারি', 2: 'ফেব্রুয়ারি', 3: 'মার্চ', 4: 'এপ্রিল',
            5: 'মে', 6: 'জুন', 7: 'জুলাই', 8: 'আগস্ট',
            9: 'সেপ্টেম্বর', 10: 'অক্টোবর', 11: 'নভেম্বর', 12: 'ডিসেম্বর'
        }
        today = datetime.now()
        bengali_date = f"{today.day} {bengali_months[today.month]} {today.year}"
        
        post = f"""🎯 ICT MCQ Challenge | {bengali_date}
━━━━━━━━━━━━━━━━━━━━

🏆 আজকের চ্যালেঞ্জ: {len(questions)} টি প্রশ্নের উত্তর দিন এবং আপনার স্কোর জানুন!

নিয়মাবলী:
• প্রতিটি সঠিক উত্তর = ১ নম্বর
• মোট নম্বর: {len(questions)}
• সময়: ১৫ মিনিট

━━━━━━━━━━━━━━━━━━━━

"""
        
        for idx, q in enumerate(questions, 1):
            post += f"প্রশ্ন {idx}:\n"
            post += f"{q['question']}\n"
            
            for option in q['options']:
                post += f"{option}\n"
            
            post += "\n"
        
        # Scoring guide
        post += """━━━━━━━━━━━━━━━━━━━━
📊 স্কোরিং গাইড:
"""
        total = len(questions)
        post += f"• {total}-{int(total*0.8)}: অসাধারণ! 🌟\n"
        post += f"• {int(total*0.79)}-{int(total*0.6)}: চমৎকার! 👏\n"
        post += f"• {int(total*0.59)}-{int(total*0.4)}: ভালো! 📚\n"
        post += f"• {int(total*0.39)} এর নিচে: আরও পড়ুন! 💪\n"
        
        post += """\n💬 উত্তর কমেন্টে শেয়ার করুন এবং আপনার স্কোর জানান!
✅ সঠিক উত্তর ১ ঘণ্টা পরে কমেন্টে দেওয়া হবে!

📱 ICT Tutor Pro App ডাউনলোড করুন:
https://play.google.com/store/apps/details...

#ICTQuizChallenge #MCQPractice #HSC #Honours #ICTTutorPro"""
        
        # Answer key for later comment
        answer_comment = "✅ সঠিক উত্তরসমূহ:\n\n"
        for idx, q in enumerate(questions, 1):
            answer_comment += f"{idx}. {q['answer']}\n"
        
        answer_comment += f"\n📊 আপনার স্কোর কত হয়েছে? কমেন্টে জানান!"
        
        return post, answer_comment
    
    def post_to_facebook(self, message, post_id=None):
        """Post to Facebook page or comment on existing post"""
        if not self.page_id or not self.access_token:
            print("❌ Facebook credentials not provided")
            return None
        
        try:
            if post_id:
                # Post comment
                url = f"https://graph.facebook.com/v18.0/{post_id}/comments"
                data = {
                    'message': message,
                    'access_token': self.access_token
                }
            else:
                # Create new post
                url = f"https://graph.facebook.com/v18.0/{self.page_id}/feed"
                data = {
                    'message': message,
                    'access_token': self.access_token
                }
            
            response = requests.post(url, data=data)
            
            if response.status_code == 200:
                result = response.json()
                if post_id:
                    print(f"✅ Comment posted successfully: {result.get('id')}")
                else:
                    print(f"✅ Post created successfully: {result.get('id')}")
                return result.get('id')
            else:
                print(f"❌ Facebook API Error: {response.status_code}")
                print(f"Response: {response.text}")
                return None
                
        except Exception as e:
            print(f"❌ Error posting to Facebook: {str(e)}")
            return None
    
    def clean_old_files(self, output_dir='output_posts', days=2):
        """Delete files older than specified days"""
        print(f"\n🧹 Cleaning files older than {days} days...")
        
        if not os.path.exists(output_dir):
            print(f"Directory {output_dir} does not exist")
            return
        
        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0
        
        for filename in os.listdir(output_dir):
            filepath = os.path.join(output_dir, filename)
            
            if os.path.isfile(filepath):
                file_modified = datetime.fromtimestamp(os.path.getmtime(filepath))
                
                if file_modified < cutoff_date:
                    try:
                        os.remove(filepath)
                        print(f"🗑️  Deleted: {filename}")
                        deleted_count += 1
                    except Exception as e:
                        print(f"❌ Error deleting {filename}: {str(e)}")
        
        print(f"✅ Cleaned {deleted_count} old files\n")
    
    def save_posts(self, posts, output_dir='output_posts'):
        """Save generated posts to files"""
        Path(output_dir).mkdir(exist_ok=True)
        
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        
        for idx, post_data in enumerate(posts, 1):
            filename = f"{output_dir}/post_{idx}_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                if isinstance(post_data, tuple):
                    f.write("=== MAIN POST ===\n\n")
                    f.write(post_data[0])
                    f.write("\n\n" + "="*50 + "\n")
                    f.write("=== COMMENT ===\n\n")
                    f.write(post_data[1])
                else:
                    f.write(post_data)
            
            print(f"✅ Post {idx} saved: {filename}")
    
    def run_post_type(self, post_type):
        """Run specific post type and post to Facebook"""
        print(f"\n{'='*60}")
        print(f"🚀 Running Post Type {post_type}")
        print(f"{'='*60}\n")
        
        # Clean old files first
        self.clean_old_files()
        
        # Select 10 random questions without images
        questions = self.get_questions_without_image(10)
        
        if not questions:
            print("❌ No questions available!")
            return
        
        print(f"📝 Selected {len(questions)} questions without images\n")
        
        # Generate and post based on type
        if post_type == 1:
            print("1️⃣ Generating Post Type 1: With Answer Keys...")
            post_content = self.post_type_1_with_answers(questions)
            
            # Save to file
            self.save_posts([post_content])
            
            # Post to Facebook
            if self.page_id and self.access_token:
                print("\n📤 Posting to Facebook...")
                self.post_to_facebook(post_content)
            
        elif post_type == 2:
            print("2️⃣ Generating Post Type 2: Questions + Comment Answers...")
            main_post, comment = self.post_type_2_questions_only(questions)
            
            # Save to file
            self.save_posts([(main_post, comment)])
            
            # Post to Facebook
            if self.page_id and self.access_token:
                print("\n📤 Posting to Facebook...")
                post_id = self.post_to_facebook(main_post)
                
                if post_id:
                    print("⏳ Waiting 5 seconds before posting comment...")
                    time.sleep(5)
                    self.post_to_facebook(comment, post_id)
            
        elif post_type == 3:
            print("3️⃣ Generating Post Type 3: Quiz Challenge...")
            main_post, answer_comment = self.post_type_3_quiz_challenge(questions)
            
            # Save to file
            self.save_posts([(main_post, answer_comment)])
            
            # Post to Facebook
            if self.page_id and self.access_token:
                print("\n📤 Posting to Facebook...")
                post_id = self.post_to_facebook(main_post)
                
                # Note: Answer comment should be posted manually after 1 hour
                print("ℹ️  Note: Post answer comment manually after 1 hour for engagement")
        
        print(f"\n✨ Post Type {post_type} completed successfully!\n")


def main():
    """Main execution function"""
    # Get credentials from environment variables
    page_id = os.environ.get('FB_PAGE_ID')
    access_token = os.environ.get('FB_ACCESS_TOKEN')
    post_type = int(os.environ.get('POST_TYPE', '1'))
    
    if not page_id or not access_token:
        print("⚠️  Warning: Facebook credentials not found in environment variables")
        print("Set FB_PAGE_ID and FB_ACCESS_TOKEN environment variables")
        print("Running in test mode (no Facebook posting)...\n")
    
    generator = MCQPostGenerator(
        json_file='jkj/main/teacher/question_bank.json',
        page_id=page_id,
        access_token=access_token
    )
    
    generator.run_post_type(post_type)


if __name__ == "__main__":
    main()