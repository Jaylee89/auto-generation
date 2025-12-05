tell application "Microsoft Edge"
    activate
    tell front window
        -- 尝试获取朗读工具栏的按钮
        try
            set readAloudButton to buttons whose description contains "朗读" or description contains "Read aloud"
            if length of readAloudButton > 0 then
                return "朗读功能已激活"
            else
                return "朗读功能未激活"
            end if
        on error
            return "无法检测"
        end try
    end tell
end tell