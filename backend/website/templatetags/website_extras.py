from datetime import datetime

from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.simple_tag
def status_badge(completed):
    if completed:
        return mark_safe(
            '<span class="inline-flex items-center gap-1 text-emerald-400 text-xs font-medium">'
            '<span class="w-1.5 h-1.5 rounded-full bg-emerald-500"></span>Done</span>'
        )
    return mark_safe(
        '<span class="inline-flex items-center gap-1 text-slate-500 text-xs font-medium">'
        '<span class="w-1.5 h-1.5 rounded-full bg-slate-600"></span>Pending</span>'
    )


@register.filter
def time_ago(value):
    now = datetime.now(value.tzinfo if value.tzinfo else None)
    diff = now - value
    if diff.days > 365:
        years = diff.days // 365
        return f"{years}y ago"
    if diff.days > 30:
        months = diff.days // 30
        return f"{months}mo ago"
    if diff.days > 0:
        return f"{diff.days}d ago"
    if diff.seconds > 3600:
        hours = diff.seconds // 3600
        return f"{hours}h ago"
    if diff.seconds > 60:
        minutes = diff.seconds // 60
        return f"{minutes}m ago"
    return "just now"


@register.filter
def trim(value):
    if isinstance(value, str):
        return value.strip()
    return value


@register.filter
def startswith(value, arg):
    return str(value).startswith(arg)


@register.filter
def endswith(value, arg):
    return str(value).endswith(arg)


@register.filter
def contains(value, arg):
    return arg in str(value)


@register.filter
def field_errors(field):
    return field.errors


@register.filter
def pluralize_count(value, arg="s"):
    if value == 1:
        return f"{value} {arg}" if not arg.endswith("s") else f"{value} {arg[:-1]}"
    return f"{value} {arg}"


@register.simple_tag
def current_time(format_str="Y-m-d H:i"):
    from datetime import datetime
    return datetime.now().strftime(format_str)


@register.simple_tag
def status_badge_status(status):
    colors = {
        "placed": "text-blue-400 bg-blue-950/40 border-blue-700/40",
        "processing": "text-amber-400 bg-amber-950/40 border-amber-700/40",
        "shipped": "text-purple-400 bg-purple-950/40 border-purple-700/40",
        "out_for_delivery": "text-cyan-400 bg-cyan-950/40 border-cyan-700/40",
        "delivered": "text-emerald-400 bg-emerald-950/40 border-emerald-700/40",
    }
    cls = colors.get(status, "text-slate-400 bg-slate-950/40 border-slate-700/40")
    label = status.replace("_", " ").title()
    return mark_safe(
        f'<span class="inline-flex items-center text-xs font-medium rounded-full px-2 py-0.5 border {cls}">{label}</span>'
    )


@register.simple_tag
def task_stats():
    from ..models import Task
    total = Task.objects.count()
    done = Task.objects.filter(completed=True).count()
    pending = total - done
    return f"{done}/{total} done ({pending} pending)"
