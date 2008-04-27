(defun mailsync/gnus-check (groups)
  "Check for new news in the groups."
  (save-excursion
    (save-window-excursion
      (switch-to-buffer "*Group*")
      (if (null groups)
          (gnus-group-get-new-news)
        (dolist (group groups)
          (gnus-group-jump-to-group group)
          (gnus-group-get-new-news-this-group))))))
