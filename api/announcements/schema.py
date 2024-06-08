announcements_schema = '''
                        CREATE TABLE IF NOT EXISTS announcements (
                        
                        id INT NOT NULL AUTO_INCREMENT,
                        PRIMARY KEY (id),

                        date_created TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

                        title VARCHAR(255) NOT NULL,

                        type ENUM('memo', 'single_event', 'multi_event') NOT NULL,

                        message VARCHAR(255) NOT NULL,

                        event_start_date DATE DEFAULT NULL,

                        event_end_date DATE DEFAULT NULL,

                        event_time TIME DEFAULT NULL,

                        CONSTRAINT check_multi_event_type CHECK (
                        type != 'multi_event' OR (event_start_date IS NOT NULL AND event_end_date IS NOT NULL)
                        ),

                        CONSTRAINT check_single_event_type CHECK (
                        type != 'single_event' OR (event_start_date IS NOT NULL AND event_end_date IS NULL AND event_time IS NOT NULL)
                        ),

                        CONSTRAINT check_memo_type CHECK (
                        type != 'memo' OR (event_start_date IS NULL AND event_end_date IS NULL AND event_time IS NULL)
                        )
                        )
                        '''