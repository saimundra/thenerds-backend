from django.contrib.auth.models import User
from django.core.management.base import BaseCommand

from api.models import Post


SEED_POSTS = [
    {
        'title': 'AI-Driven Alpha: How Quant Funds Are Outperforming in 2026',
        'slug': 'ai-driven-alpha-2026',
        'category': 'Financial Research',
        'status': 'published',
        'author': 'Marcus Chen',
        'date': 'Apr 14, 2026',
        'read_time': '8 min',
        'meta_title': 'AI-Driven Alpha: Quant Fund Outperformance in 2026 | The.Nerds',
        'meta_description': 'Analysis of 14 quant funds over 18 months shows alternative data integration generates 340bps excess return.',
        'h1': 'AI-Driven Alpha: How Quant Funds Are Outperforming in 2026',
        'alt_text': 'Abstract financial data visualization with glowing blue quantitative analysis lines on dark background',
        'views': 4820,
        'image': 'https://img.rocket.new/generatedImages/rocket_gen_img_1ccd712fd-1766948375555.png',
    },
    {
        'title': 'The Emerging Market Inflection Point: 3 Signals Worth Watching',
        'slug': 'emerging-market-inflection',
        'category': 'Market Analysis',
        'status': 'published',
        'author': 'Priya Nair',
        'date': 'Apr 8, 2026',
        'read_time': '6 min',
        'meta_title': 'Emerging Market Inflection Point: 3 Key Signals | The.Nerds',
        'meta_description': 'Currency reserves, yield differentials, and FDI flows signal a pattern not seen since 2009.',
        'h1': 'The Emerging Market Inflection Point: 3 Signals Worth Watching',
        'alt_text': 'Global financial network map with data connection lines on dark blue background',
        'views': 3210,
        'image': 'https://img.rocket.new/generatedImages/rocket_gen_img_121f9f371-1764679233420.png',
    },
    {
        'title': "Data Moats in SaaS: Who's Building Defensible Advantages",
        'slug': 'data-moats-saas-2026',
        'category': 'Competitive Intel',
        'status': 'draft',
        'author': 'James Okafor',
        'date': 'Mar 29, 2026',
        'read_time': '11 min',
        'meta_title': 'Data Moats in SaaS 2026: Defensible Competitive Advantages | The.Nerds',
        'meta_description': "Mapping 60 SaaS companies to identify who's building durable competitive advantages through proprietary data.",
        'h1': 'Data Moats in SaaS: Which Companies Are Building Defensible Advantages',
        'alt_text': 'Dark analytics dashboard with competitive analysis charts and blue data visualization',
        'views': 0,
        'image': 'https://images.unsplash.com/photo-1526628953301-3e589a6a8b74',
    },
    {
        'title': 'Fed Policy in 2026: Three Scenarios and Their Market Implications',
        'slug': 'fed-policy-2026-outlook',
        'category': 'Macro',
        'status': 'published',
        'author': 'Sophia Reyes',
        'date': 'Mar 22, 2026',
        'read_time': '9 min',
        'meta_title': 'Fed Policy 2026: Three Scenarios for Markets | The.Nerds',
        'meta_description': 'We model three Fed rate scenarios and their cascading effects on equity, credit, and FX markets.',
        'h1': 'Fed Policy in 2026: Three Scenarios and Their Market Implications',
        'alt_text': 'Financial trader analyzing macroeconomic charts on multiple dark screens with blue atmospheric glow',
        'views': 2890,
        'image': 'https://img.rocket.new/generatedImages/rocket_gen_img_14d508a3d-1773183116504.png',
    },
    {
        'title': 'Private Credit: The $2T Opportunity That Banks Are Leaving Behind',
        'slug': 'private-credit-opportunity',
        'category': 'Financial Research',
        'status': 'draft',
        'author': 'Priya Nair',
        'date': 'Mar 8, 2026',
        'read_time': '7 min',
        'meta_title': 'Private Credit: $2T Opportunity in Middle-Market Lending | The.Nerds',
        'meta_description': 'Regional bank retrenchment creates structural supply gap in middle-market lending with compelling risk-adjusted returns.',
        'h1': 'Private Credit: The $2T Opportunity That Banks Are Leaving Behind',
        'alt_text': 'Financial research documents and investment analysis charts on dark professional desk environment',
        'views': 0,
        'image': 'https://img.rocket.new/generatedImages/rocket_gen_img_1252c4357-1773132728301.png',
    },
    {
        'title': 'The Alternative Data Edge: Which Sources Actually Move Markets',
        'slug': 'alt-data-edge-2026',
        'category': 'Data Analytics',
        'status': 'published',
        'author': 'Marcus Chen',
        'date': 'Mar 15, 2026',
        'read_time': '13 min',
        'meta_title': 'Alternative Data Edge 2026: Which Sources Move Markets | The.Nerds',
        'meta_description': 'After backtesting 40 data sources, only 11 showed consistent predictive power across multiple market cycles.',
        'h1': 'The Alternative Data Edge: Which Sources Actually Move Markets',
        'alt_text': 'Data analysis workspace with multiple screens showing quantitative models and financial charts',
        'views': 1980,
        'image': 'https://img.rocket.new/generatedImages/rocket_gen_img_17592cde9-1767269946295.png',
    },
    {
        'title': 'Semiconductor Cycle: Where Are We Now and What Comes Next',
        'slug': 'semiconductor-cycle-2026',
        'category': 'Market Analysis',
        'status': 'published',
        'author': 'James Okafor',
        'date': 'Feb 28, 2026',
        'read_time': '10 min',
        'meta_title': 'Semiconductor Cycle 2026: Current Phase and Next Upcycle | The.Nerds',
        'meta_description': 'Lead times, book-to-bill ratios, and capex signals point to the next semiconductor upcycle starting in Q3 2026.',
        'h1': 'Semiconductor Cycle: Where Are We Now and What Comes Next',
        'alt_text': 'Semiconductor chip close-up with blue circuit patterns on dark background',
        'views': 1675,
        'image': 'https://images.unsplash.com/photo-1697071337274-2e7db58d8b5e',
    },
]


class Command(BaseCommand):
    help = 'Seed default user and blog posts for local development.'

    def handle(self, *args, **kwargs):
        username = 'admin'
        password = 'Admin@12345'
        email = 'admin@thenerds.local'

        user, created = User.objects.get_or_create(username=username, defaults={'email': email})
        user.set_password(password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        for post in SEED_POSTS:
            Post.objects.update_or_create(slug=post['slug'], defaults=post)

        self.stdout.write(self.style.SUCCESS('Seed complete.'))
        self.stdout.write(self.style.SUCCESS(f'Login username: {username}'))
        self.stdout.write(self.style.SUCCESS(f'Login password: {password}'))