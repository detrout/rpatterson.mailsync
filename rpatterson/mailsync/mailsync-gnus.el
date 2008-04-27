(defun mailsync/gnus-check (groups)
  "Check for new news in the groups."
  (switch-to-buffer "*Group*")
  (dolist (group groups)
    (gnus-group-jump-to-group group)
    (gnus-group-get-new-news-this-group)))
