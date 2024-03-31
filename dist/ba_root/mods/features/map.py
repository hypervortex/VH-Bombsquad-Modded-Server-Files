import ba, _ba

class TEXTONMAP:
    def __init__(self):
        if hasattr(_ba, "season_ends_in_days"):
            self._remaining_time = self._get_remaining_time(_ba.season_ends_in_days)
            self._text_node = None
            self._update_timer = None
            self.season_reset(self._remaining_time)

    def _get_remaining_time(self, days):
        seconds_per_day = 86400  # 24 hours * 60 minutes * 60 seconds
        remaining_seconds = days * seconds_per_day
        remaining_days = remaining_seconds // seconds_per_day
        remaining_seconds %= seconds_per_day
        remaining_hours = remaining_seconds // 3600
        remaining_seconds %= 3600
        remaining_minutes = remaining_seconds // 60
        remaining_seconds %= 60
        return remaining_days, remaining_hours, remaining_minutes, remaining_seconds

    def season_reset(self, remaining_time):
        days, hours, minutes, seconds = remaining_time
        self._text_node = ba.newnode('text',
                                     attrs={
                                         'text': f"Season ends in: {days} days, {hours:02d}:{minutes:02d}:{seconds:02d}",
                                         'flatness': 1.0,
                                         'h_align': 'right',
                                         'v_attach': 'bottom',
                                         'h_attach': 'right',
                                         'scale': 0.7,
                                         'position': (-25, 45),
                                         'color': (1, 0.5, 0.7)
                                     })

        self._update_timer = ba.timer(1.0, self._update_text, repeat=True)

    def _update_text(self):
        if self._remaining_time[0] > 0:
            days, hours, minutes, seconds = self._remaining_time
            total_seconds = days * 86400 + hours * 3600 + minutes * 60 + seconds
            total_seconds -= 1
            remaining_days = total_seconds // 86400
            remaining_hours = (total_seconds % 86400) // 3600
            remaining_minutes = (total_seconds % 3600) // 60
            remaining_seconds = total_seconds % 60
            self._remaining_time = remaining_days, remaining_hours, remaining_minutes, remaining_seconds
            self._text_node.text = f'Season ends in: {days} days, {hours:02d}:{minutes:02d}:{seconds:02d}'
        else:
            ba.print_error('Error: Remaining days cannot be negative.')
            self._text_node.delete()
            self._update_timer = None
