
from django.shortcuts import render, redirect
from django.contrib.auth import  authenticate, login as auth_login
from django.contrib.auth import logout, authenticate, login as auth_login
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .forms import SignupForm
from django.urls import reverse
from django.contrib.auth.models import User
from .models import Branch, SalesRepresentative
from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password



################HOME PAGE##############
def home(request):
    products = [
        {'img': 'product1.jpg', 'title': 'Box Profile Mabati', 'desc': 'Strong and sleek.', 'price': 'Ksh 1,200/sheet'},
        {'img': 'product2.png', 'title': 'Corrugated Mabati', 'desc': 'Classic and affordable.', 'price': 'Ksh 1,050/sheet'},
        {'img': 'product3.png', 'title': 'Tile Profile Mabati', 'desc': 'Elegant and durable.', 'price': 'Ksh 1,300/sheet'}
    ]
    return render(request, 'home.html', {'products': products})


from django.contrib.auth import authenticate, login as auth_login
from django.contrib import messages
from django.shortcuts import redirect
from django.urls import reverse
from django.contrib.auth.models import User

def signin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Ensure email and password are provided
        if not email or not password:
            messages.error(request, "Both email and password are required.", extra_tags="login_error")
            return redirect('signin')

        # Get user by email
        user = User.objects.filter(email=email).first()

        if user:
            authenticated_user = authenticate(request, username=user.username, password=password)
            if authenticated_user:
                # Check if the authenticated user is a superuser
                if authenticated_user.is_superuser:
                    auth_login(request, authenticated_user)
                    return redirect(reverse('operations'))  # Redirect to dashboard
                else:
                    messages.error(request, "You do not have permission to access this page.", extra_tags="login_error")
                    return redirect('signin')  # Redirect back to the signin page
            else:
                messages.error(request, "Invalid email or password.", extra_tags="login_error")
        else:
            messages.error(request, "Invalid email or password.", extra_tags="login_error")

    return render(request, 'signing.html')  # Ensure the correct template name




from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from .models import Sale, SalesRepresentative, Branch
from django.contrib import messages

@login_required
def operations(request):
    sales_reps = list(SalesRepresentative.objects.all())

    # Include logged-in user in the display if not already a sales rep
    if not any(rep.user == request.user for rep in sales_reps):
        temp_rep = SalesRepresentative(user=request.user)
        sales_reps.append(temp_rep)

    branches = Branch.objects.all()

    if request.method == 'POST':
        try:
            # Get and validate form inputs
            customer_name = request.POST.get('customer_name', '').strip()
            total_amount = float(request.POST.get('total_amount', '0'))
            invoice_amount = float(request.POST.get('invoice_amount', '0'))
            amount_paid = float(request.POST.get('amount_paid', '0'))
            balance = float(request.POST.get('balance', '0'))
            profit = float(request.POST.get('profit', '0'))
            place_of_delivery = request.POST.get('place_of_delivery', '').strip()
            payment_status = request.POST.get('payment_status', '').strip()

            sales_rep_id = request.POST.get('sales_rep')
            branch_id = request.POST.get('branch')

            if not sales_rep_id or not branch_id:
                messages.error(request, "Please select both a Sales Representative and a Branch.")
                raise ValueError("Missing related fields")

            sales_rep = SalesRepresentative.objects.get(id=sales_rep_id)
            branch = Branch.objects.get(id=branch_id)

            # Save the Sale record
            Sale.objects.create(
                customer_name=customer_name,
                total_amount=total_amount,
                invoice_amount=invoice_amount,
                amount_paid=amount_paid,
                balance=balance,
                profit=profit,
                place_of_delivery=place_of_delivery,
                payment_status=payment_status,
                sales_rep=sales_rep,
                branch=branch,
                user=request.user
            )

            messages.success(request, "Sale recorded successfully!")
            return redirect('operations')

        except ValueError as ve:
            messages.error(request, f"Invalid input: {ve}")
        except SalesRepresentative.DoesNotExist:
            messages.error(request, "Selected Sales Representative does not exist.")
        except Branch.DoesNotExist:
            messages.error(request, "Selected Branch does not exist.")
        except Exception as e:
            messages.error(request, f"Something went wrong: {e}")

    return render(request, 'operations.html', {
        'sales_reps': sales_reps,
        'branches': branches,
    })



@login_required
def sales_reps(request):
    branches = Branch.objects.all()

    if request.method == 'POST':
        # Extract data
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        username = request.POST.get('username')
        password = request.POST.get('password')
        branch_id = request.POST.get('branch')

        # Create User
        user = User.objects.create(
            username=username,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=make_password(password),
        )

        # Create SalesRep and link to creator
        branch = Branch.objects.get(id=branch_id)
        SalesRepresentative.objects.create(
            user=user,
            phone=phone,
            branch=branch,
            created_by=request.user  # capture the logged-in user
        )

        return redirect('sales_reps')  # Change redirect target as needed

    return render(request, 'sales_reps.html', {'branches': branches})





@login_required
def add_branch(request):
    if request.method == 'POST':
        name = request.POST.get('branch_name')
        location = request.POST.get('branch_location')

        # Save to DB with the logged-in user
        Branch.objects.create(name=name, location=location, user=request.user)
        return redirect('add_branch')

    return render(request, 'add_branch.html')

def logout_view(request):
    logout(request)  # Logs out the user
    return redirect('home')  # Redirect to the home page


from django.shortcuts import render
from django.db.models import Sum
from .models import Sale, SalesRepresentative, Branch
from django.utils import timezone

# Add the utility function
def format_number(num):
    """
    Formats a large number to a more readable format with K (thousands), M (millions), B (billions).
    """
    if num >= 1_000_000_000:
        return f'{num / 1_000_000_000:.1f}B'
    elif num >= 1_000_000:
        return f'{num / 1_000_000:.1f}M'
    elif num >= 1_000:
        return f'{num / 1_000:.1f}K'
    else:
        return str(num)

def reports(request):
    # Get the logged-in user
    user = request.user
    
    sales_reps = SalesRepresentative.objects.filter()
    
    branches = Branch.objects.filter()

    # Get sales data for the logged-in user
    sales = Sale.objects.filter()

    # Calculate total customers (distinct customer names)
    total_customers = sales.values('customer_name').distinct().count()

    # Calculate total sales amount
    total_sales = sales.aggregate(Sum('invoice_amount'))['invoice_amount__sum'] or 0  # Use 0 if no sales found
    total_sales_formatted = format_number(total_sales)  # Format total sales amount

    # Calculate total profit
    total_profit = sales.aggregate(Sum('profit'))['profit__sum'] or 0
    total_profit_formatted = format_number(total_profit)  # Format total profit
    
    # Calculate total balances
    total_balance = sales.aggregate(Sum('balance'))['balance__sum'] or 0
    total_balance_formatted = format_number(total_balance)  # Format total profit

    # Calculate total sales representatives (distinct)
    total_sales_reps = SalesRepresentative.objects.filter().count()

    # Calculate total branches (distinct)
    total_branches = Branch.objects.filter().count()

    # Get current month
    current_month = timezone.now().month

    # Calculate total sales for the current month
    total_sales_current_month = sales.filter(created_at__month=current_month).aggregate(Sum('invoice_amount'))['invoice_amount__sum'] or 0
    total_sales_current_month_formatted = format_number(total_sales_current_month)  # Format current month's sales amount

    return render(request, 'reports.html', {
        'sales': sales,
        'sales_reps': sales_reps,
        'branches': branches,  # Corrected key here
        'total_customers': total_customers,
        'total_sales': total_sales_formatted,  # Pass the formatted value
        'total_sales_current_month': total_sales_current_month_formatted,  # Pass the formatted value
        'total_profit': total_profit_formatted,  # Pass the formatted value for profit
        'total_balance': total_balance_formatted,  # Pass the formatted value for profit
        'total_sales_reps': total_sales_reps,  # Pass the total sales representatives
        'total_branches': total_branches,  # Pass the total branches
    })
