class Config:
    # Upload Settings
    UPLOAD_FOLDER = 'uploads'
    ALLOWED_EXTENSIONS = {'txt', 'pdf', 'docx'}
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024

    # Algorithm Defaults
    DEFAULT_WEIGHTS = {
        'skills': 0.4,
        'experience': 0.3,
        'education': 0.3
    }

    # Visualization
    PLOT_STYLE = 'ggplot'
