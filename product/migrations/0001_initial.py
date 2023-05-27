# Generated by Django 4.2.1 on 2023-05-27 13:19

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='عنوان دسته بندی')),
                ('slug', models.SlugField(allow_unicode=True, blank=True, null=True, unique=True, verbose_name='اسلاگ')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True, verbose_name='تاریخ ایجاد دسته بندی')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='product.category', verbose_name='زیردسته')),
            ],
            options={
                'verbose_name': 'دسته بندی',
                'verbose_name_plural': 'دسته بندی\u200c ها',
                'ordering': ['parent__id'],
            },
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.CharField(max_length=30, primary_key=True, serialize=False, unique=True, verbose_name='کد محصول')),
                ('title', models.CharField(max_length=100, verbose_name='عنوان محصول')),
                ('country', models.CharField(max_length=50, verbose_name='کشور')),
                ('description', models.TextField(verbose_name='توضیحات')),
                ('price', models.PositiveIntegerField(default=0, verbose_name='قیمت (ریال)')),
                ('discount', models.PositiveIntegerField(blank=True, null=True, verbose_name='درصد تخفیف')),
                ('weight', models.CharField(max_length=30, verbose_name='وزن')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('category', models.ManyToManyField(related_name='categories', to='product.category', verbose_name='دسته بندی')),
            ],
            options={
                'verbose_name': 'محصول',
                'verbose_name_plural': 'محصولات',
                'ordering': ('-created_at',),
            },
        ),
        migrations.CreateModel(
            name='Spec',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('battery_capacity', models.CharField(blank=True, max_length=30, null=True, verbose_name='ظرفیت باتری (ولت)')),
                ('injection_force', models.CharField(blank=True, max_length=30, null=True, verbose_name='نیروی تزریق (نیوتن)')),
                ('grease_capacity', models.CharField(blank=True, max_length=30, null=True, verbose_name='ظرفیت گریس (گرم)')),
                ('hose_size', models.CharField(blank=True, max_length=30, null=True, verbose_name='اندازه خرطوم (میلی متر)')),
                ('hit_rate', models.CharField(blank=True, max_length=30, null=True, verbose_name='میزان ضربه (ضربه در دقیقه)')),
                ('chuck_size', models.CharField(blank=True, max_length=30, null=True, verbose_name='اندازه سه نظام (میلی متر)')),
                ('surface_diameter', models.CharField(blank=True, max_length=30, null=True, verbose_name='قطر صفحه (میلی متر)')),
                ('speed_range', models.CharField(blank=True, max_length=30, null=True, verbose_name='بازه سرعتی (دور بر دقیقه)')),
                ('storage_capacity', models.CharField(blank=True, max_length=30, null=True, verbose_name='ظرفیت مخزن (میلی لیتر)')),
                ('max_cut_depth', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر عمق برش (میلی متر)')),
                ('maximum_torque', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر گشتاور (نیوتن متر)')),
                ('injection_rate', models.CharField(blank=True, max_length=30, null=True, verbose_name='نرخ تزریق (میلی متر بر دقیقه)')),
                ('injection_speed', models.CharField(blank=True, max_length=30, null=True, verbose_name='سرعت تزریق (میلی متر بر دقیقه)')),
                ('tip_holder_size', models.CharField(blank=True, max_length=30, null=True, verbose_name='اندازه نگهدارنده نوک (میلی متر)')),
                ('angle', models.CharField(blank=True, max_length=30, null=True, verbose_name='زاویه (درجه)')),
                ('grease_type', models.CharField(blank=True, max_length=30, null=True, verbose_name='نوع گریس')),
                ('gear_count', models.CharField(blank=True, max_length=30, null=True, verbose_name='تعداد دور')),
                ('hit_force', models.CharField(blank=True, max_length=30, null=True, verbose_name='قدرت ضربه (ژول)')),
                ('dimensions', models.CharField(blank=True, max_length=50, null=True, verbose_name='ابعاد (میلی متر)')),
                ('input_watt', models.CharField(blank=True, max_length=30, null=True, verbose_name='توان ورودی (وات)')),
                ('heat_range', models.CharField(blank=True, max_length=30, null=True, verbose_name='بازه حرارتی (ولت)')),
                ('max_angle', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر زاویه (درجه)')),
                ('working_modes', models.CharField(blank=True, max_length=200, null=True, verbose_name='حالت\u200cهای کار کردن')),
                ('base_size', models.CharField(blank=True, max_length=30, null=True, verbose_name='اندازه پایه (میلی متر)')),
                ('colette_size', models.CharField(blank=True, max_length=30, null=True, verbose_name='سایز کولت (میلی متر)')),
                ('rock_thickness', models.CharField(blank=True, max_length=30, null=True, verbose_name='ضخامت سنگ (میلی متر)')),
                ('wind_force', models.CharField(blank=True, max_length=30, null=True, verbose_name='قدرت پخش باد (کیلوگرم)')),
                ('blow_force', models.CharField(blank=True, max_length=30, null=True, verbose_name='قدرت دمندگی (میلی متر)')),
                ('shake_rate', models.CharField(blank=True, max_length=30, null=True, verbose_name='نرخ لرزش (لرزش بر دقیقه)')),
                ('grating_depth', models.CharField(blank=True, max_length=30, null=True, verbose_name='عمق رنده کاری (میلی متر)')),
                ('cutting_angle_range', models.CharField(blank=True, max_length=30, null=True, verbose_name='بازه زاویه برش (درجه)')),
                ('grating_rate', models.CharField(blank=True, max_length=30, null=True, verbose_name='نرخ رنده کاری (متر بر دقیقه)')),
                ('sandpaper_dimensions', models.CharField(blank=True, max_length=30, null=True, verbose_name='ابعاد سنباده (میلی متر)')),
                ('max_surface_diameter', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر قطر صفحه (میلی متر)')),
                ('working_table_dimensions', models.CharField(blank=True, max_length=30, null=True, verbose_name='ابعاد میز کار (میلی متر)')),
                ('max_hole_water', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر قطر سوراخکاری با آب (میلی متر)')),
                ('sanding_circuit_length', models.CharField(blank=True, max_length=30, null=True, verbose_name='طول مدار سنباده زنی (میلی متر)')),
                ('max_work_tool_dimensions', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر قطر قطعه کار (میلی متر)')),
                ('max_cut_depth_wood', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر عمق برش در چوب (میلی متر)')),
                ('max_cut_depth_iron', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر عمق برش در آهن (میلی متر)')),
                ('vibration_rate', models.CharField(blank=True, max_length=30, null=True, verbose_name='میزان ویبراسیون حین کار (m/s2)')),
                ('max_screw_diameter', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر قطر پیچ (میلی متر)')),
                ('tool_holder_size', models.CharField(blank=True, max_length=30, null=True, verbose_name='اندازه ابزارگیر (میلی متر)')),
                ('max_hole_not_water', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر قطر سوراخکاری بدون آب (میلی متر)')),
                ('max_45_90_angle', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر عمق برش در زوایای ۴۵ و ۹۰ (میلی متر)')),
                ('max_hole_diameter_wood_iron', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر قطر سوراخ در چوب و آهن (میلی متر)')),
                ('max_hole_cutting_tool', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر قطر سوراخکاری با ابزار برش (میلی متر)')),
                ('max_hole_diameter_wood_concrete', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر قطر سوراخ در بتن (میلی متر)')),
                ('max_depth_cutting_tool', models.CharField(blank=True, max_length=30, null=True, verbose_name='حداکثر عمق سوراخکاری با ابزار برش (میلی متر)')),
                ('force_to_hole', models.CharField(blank=True, max_length=30, null=True, verbose_name='میزان نیروی وارده به محل سوراخکاری (کیلوگرم)')),
                ('has_box', models.BooleanField(default=False, verbose_name='جعبه دارد')),
                ('has_dimmer', models.BooleanField(default=False, verbose_name='دیمر دار')),
                ('has_hammer_mode', models.BooleanField(default=False, verbose_name='حالت چکشی')),
                ('has_spare_battery', models.BooleanField(default=False, verbose_name='باتری یدک')),
                ('has_safe_start', models.BooleanField(default=False, verbose_name='شروع ایمن دارد')),
                ('is_brushless_mototr', models.BooleanField(default=False, verbose_name='سیستم بدون ذغال')),
                ('has_left_right_movement', models.BooleanField(default=False, verbose_name='گردش چپ راست')),
                ('excessive_watt_protection', models.BooleanField(default=False, verbose_name='محافظ اضافه بار')),
                ('product', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='specifications', to='product.product', verbose_name='محصول')),
            ],
            options={
                'verbose_name': 'مشخصه فنی',
                'verbose_name_plural': 'مشخصات فنی',
            },
        ),
        migrations.CreateModel(
            name='Picture',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('picture', models.ImageField(upload_to='products/img/', verbose_name='تصویر محصول')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='pictures', to='product.product')),
            ],
            options={
                'verbose_name': 'تصویر محصول',
                'verbose_name_plural': 'تصویر محصول',
            },
        ),
        migrations.CreateModel(
            name='Favorite',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to='product.product', verbose_name='محصول')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favorites', to=settings.AUTH_USER_MODEL, verbose_name='کاربر')),
            ],
            options={
                'verbose_name': 'علاقه مندی',
                'verbose_name_plural': 'علاقه مندی ها',
            },
        ),
        migrations.CreateModel(
            name='AdditionalItems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item', models.CharField(max_length=155, verbose_name='آیتم محصول')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='product.product')),
            ],
            options={
                'verbose_name': 'آیتم اضافی',
                'verbose_name_plural': 'آیتم های اضافی',
            },
        ),
    ]
