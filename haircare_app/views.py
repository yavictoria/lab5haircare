from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.contrib.auth import login
from .forms import RegistrationForm, HairProfileForm
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import HairProfile
from django.shortcuts import render, redirect, get_object_or_404
from .models import JournalEntry
from .forms import JournalEntryForm
from .models import AIChatMessage
from django.contrib.auth.decorators import login_required
import google.generativeai as genai
from django.conf import settings
from django.http import JsonResponse
import PIL.Image
import os



@login_required
def home(request):
    hair_profile = getattr(request.user, 'hairprofile', None)

    # Генерація рекомендацій на основі HairProfile
    recommendations = []

    if hair_profile:
        # Рекомендації для типу волосся
        if hair_profile.hair_type == "curly":
            recommendations.append("Ваше волосся кучеряве, тому мийте його 1-2 рази на тиждень, щоб уникнути сухості.")
            recommendations.append("Використовуйте маски для волосся раз на тиждень для додаткового зволоження.")
        elif hair_profile.hair_type == "straight":
            recommendations.append("Ваше волосся пряме, тому мийте його 2-3 рази на тиждень.")
            recommendations.append("Використовуйте легкі кондиціонери, щоб уникнути завантаження волосся.")

        # Рекомендації для довжини волосся
        if hair_profile.hair_length == "long":
            recommendations.append("Через довжину волосся рекомендується використовувати несмивні засоби для захисту кінчиків.")
        elif hair_profile.hair_length == "short":
            recommendations.append("Коротке волосся можна мити частіше, 3-4 рази на тиждень.")

        # Рекомендації для пористості
        if hair_profile.porosity == "high":
            recommendations.append("Ваше волосся має високу пористість, тому використовуйте зволожуючі маски та олії.")
        elif hair_profile.porosity == "low":
            recommendations.append("Ваше волосся має низьку пористість, тому уникайте важких продуктів, які можуть завантажувати волосся.")

        # Рекомендації для ламкості
        if hair_profile.brittleness == "high":
            recommendations.append("Ваше волосся схильне до ламкості, тому уникайте гарячих інструментів, таких як фен або праска.")
        elif hair_profile.brittleness == "mild":
            recommendations.append("Ваше волосся має помірну ламкість, тому використовуйте термозахисні засоби під час сушіння феном.")

        # Рекомендації для фарбованого волосся
        if hair_profile.dyed:
            recommendations.append("Ваше волосся фарбоване, тому використовуйте спеціальні шампуні для фарбованого волосся.")
        else:
            recommendations.append("Ваше волосся не фарбоване, тому ви можете використовувати звичайні засоби для догляду.")

        # Нові рекомендації

        # Частота миття голови
        if hair_profile.hair_type == "curly":
            recommendations.append("Рекомендується мити голову 1-2 рази на тиждень.")
        elif hair_profile.hair_type == "straight":
            recommendations.append("Рекомендується мити голову 2-3 рази на тиждень.")
        elif hair_profile.hair_type == "wavy":
            recommendations.append("Рекомендується мити голову 2 рази на тиждень.")

        # Скрабування шкіри голови
        if hair_profile.porosity == "high":
            recommendations.append("Скрабуйте шкіру голови раз на тиждень для видалення відмерлих клітин.")
        elif hair_profile.porosity == "low":
            recommendations.append("Скрабування шкіри голови не є обов'язковим, але можна робити це раз на 2 тижні.")

        # Частота нанесення масок
        if hair_profile.hair_type == "curly":
            recommendations.append("Використовуйте маски для волосся раз на тиждень.")
        elif hair_profile.hair_type == "straight":
            recommendations.append("Використовуйте маски для волосся раз на тиждень або двічі на тиждень, якщо волосся сухе.")

        # Використання фена
        if hair_profile.brittleness == "high":
            recommendations.append("Уникайте використання фена. Якщо це необхідно, використовуйте термозахисні засоби.")
        elif hair_profile.brittleness == "mild":
            recommendations.append("Використовуйте фен з обережністю, завжди з термозахисними засобами.")

        # Рекомендовані засоби
        if hair_profile.porosity == "high":
            recommendations.append("Використовуйте зволожуючі шампуні та кондиціонери.")
        elif hair_profile.porosity == "low":
            recommendations.append("Використовуйте легкі шампуні без сульфатів.")

        # Тип розчісування
        if hair_profile.hair_type == "curly":
            recommendations.append("Використовуйте гребінець із широкими зубцями для розчісування.")
        elif hair_profile.hair_type == "straight":
            recommendations.append("Використовуйте щітку з натуральної щетини для розчісування.")
        recommendations.append("Не розчісуйте волосся мокрим, щоб уникнути пошкоджень.")

        # Додатковий догляд
        recommendations.append("Робіть масаж голови для покращення кровообігу.")
        if hair_profile.hair_type == "curly":
            recommendations.append("Використовуйте нічний догляд, наприклад, шовкові наволочки або олії для кінчиків.")
        elif hair_profile.hair_type == "straight":
            recommendations.append("Використовуйте сироватки для блиску волосся.")

    # Fallback: generic daily tips when no profile or no recommendations
    if not recommendations:
        recommendations = [
            "Мийте волосся теплою, а не гарячою водою, щоб зберегти натуральні олії.",
            "Наносите маску на волосся від середини до кінчиків, уникаючи коренів.",
            "Робіть масаж шкіри голови кілька хвилин перед миттям для кращого кровообігу.",
            "Захищайте волосся від сонця головним убором або спреєм з SPF.",
            "Оберіть шампунь без сульфатів для м’якого щоденного догляду.",
        ]

    display_name = hair_profile.nickname if hair_profile else request.user.username

    return render(request, 'home.html', {
        'hair_profile': hair_profile,
        'recommendations': recommendations,
        'display_name': display_name,
    })


def welcome(request):
    return render(request, 'welcome.html')


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = RegistrationForm()
    return render(request, 'register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def profile(request):
    """Редагування профілю без виходу зі сторінки після збереження"""
    hair_profile, created = HairProfile.objects.get_or_create(user=request.user)  # Отримуємо або створюємо профіль

    if request.method == 'POST':
        form = HairProfileForm(request.POST, instance=hair_profile)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully!")  # Повідомлення про збереження
    else:
        form = HairProfileForm(instance=hair_profile)

    return render(request, 'profile.html', {'form': form})


def welcome_view(request):
    if request.user.is_authenticated:
        return redirect('profile')  # Перенаправляємо, якщо вже увійшов
    return render(request, 'welcome.html')


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('profile')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


@login_required
def journal_list(request):
    entries = JournalEntry.objects.filter(user=request.user).order_by('-date')
    return render(request, 'journal_list.html', {'entries': entries})

@login_required
def journal_add(request):
    if request.method == 'POST':
        form = JournalEntryForm(request.POST, request.FILES)
        if form.is_valid():
            entry = form.save(commit=False)
            entry.user = request.user
            entry.save()
            return redirect('journal_list')
    else:
        form = JournalEntryForm()
    return render(request, 'journal_form.html', {'form': form})

@login_required
def journal_delete(request, pk):
    entry = get_object_or_404(JournalEntry, pk=pk, user=request.user)
    if request.method == 'POST':
        entry.delete()
        return redirect('journal_list')
    return render(request, 'journal_confirm_delete.html', {'entry': entry})

@login_required(login_url='login')
def ai_assistant(request):
    if request.method == "POST":
        user_message = request.POST.get('message')

        # 1. Беремо базові дані профілю
        try:
            profile = request.user.hairprofile
            hair_context = f"Тип: {profile.hair_type}, Довжина: {profile.hair_length}, Пористість: {profile.porosity}, Ламкість: {profile.brittleness}, Фарбоване: {'Так' if profile.dyed else 'Ні'}."
        except Exception as e:
            hair_context = "Дані профілю не заповнені."

        # 2. АНАЛІЗ ЩОДЕННИКА (Текст + Фото)
        journal_text = ""
        images_to_send = []
        
        try:
            # ВИПРАВЛЕНО: Тепер використовуємо правильний related_name з твого models.py
            recent_entries = request.user.journal_entries.all().order_by('-date')[:5] 
            
            if recent_entries.exists():
                journal_text = "\n\nОсь останні записи зі щоденника догляду користувача (для контексту):\n"
                for entry in recent_entries:
                    journal_text += f"- Дата: {entry.date.strftime('%d.%m.%Y')}. Процедура: {entry.get_entry_type_display()}. Нотатки: {entry.notes}\n"
                    
                    # Відкриваємо фото, якщо воно є
                    if entry.photo and hasattr(entry.photo, 'path') and os.path.exists(entry.photo.path):
                        img = PIL.Image.open(entry.photo.path)
                        images_to_send.append(img)
                
                # Обмежуємо до 3 останніх фотографій, щоб AI відповідав швидко
                images_to_send = images_to_send[:3]
        except Exception as e:
            print(f"🚨 Помилка читання щоденника: {e}")

        # 3. Підключаємось до Gemini
        genai.configure(api_key=settings.GEMINI_API_KEY)

        system_instruction = f"""
        Ти — емпатичний, професійний та сучасний AI-експерт з догляду за волоссям. Твоє ім'я — Кера.
        Характеристики волосся клієнта: {hair_context}.{journal_text}
        
        ВАЖЛИВО: Разом із цим повідомленням ти можеш отримати фотографії. Це реальні фото волосся клієнта з його щоденника догляду. 
        Якщо клієнт питає про свій прогрес, стан волосся на фото або про свої минулі процедури, спирайся на ці фото та записи зі щоденника.
        Давай чіткі, дієві поради. Спілкуйся виключно українською мовою. Твій тон: дружній, підтримуючий, естетичний.
        Пиши короткими абзацами. Ніколи не використовуй маркдаун для заголовків (#).
        """

        model = genai.GenerativeModel(
            model_name='gemini-2.5-flash',
            system_instruction=system_instruction
        )

        try:
            # 4. Формуємо фінальний запит: Текст користувача + Список фотографій зі щоденника
            request_content = [user_message] + images_to_send
            
            # Відправляємо все разом в AI
            response = model.generate_content(request_content)
            ai_reply = response.text
            
            from .models import AIChatMessage
            AIChatMessage.objects.create(
                user=request.user,
                user_text=user_message,
                ai_text=ai_reply
            )

            return JsonResponse({'reply': ai_reply})
        except Exception as e:
            print(f"Помилка Gemini: {e}")
            return JsonResponse({'reply': 'Ой, щось пішло не так із зв\'язком. Спробуй ще раз трохи пізніше!'}, status=500)

    # ДЛЯ GET ЗАПИТІВ (Вивід історії)
    from .models import AIChatMessage
    chat_history = AIChatMessage.objects.filter(user=request.user).order_by('created_at')
    return render(request, 'assistant.html', {'chat_history': chat_history})