// 主JavaScript文件

// 当文档加载完成时执行
document.addEventListener('DOMContentLoaded', function() {
    // 自动隐藏消息提醒
    setTimeout(function() {
        var alerts = document.querySelectorAll('.alert');
        alerts.forEach(function(alert) {
            var bsAlert = new bootstrap.Alert(alert);
            bsAlert.close();
        });
    }, 5000);

    // 表单验证
    var forms = document.querySelectorAll('.needs-validation');
    Array.prototype.slice.call(forms).forEach(function(form) {
        form.addEventListener('submit', function(event) {
            if (!form.checkValidity()) {
                event.preventDefault();
                event.stopPropagation();
            }
            form.classList.add('was-validated');
        }, false);
    });

    // 确认删除对话框增强
    var deleteButtons = document.querySelectorAll('.btn-delete');
    deleteButtons.forEach(function(button) {
        button.addEventListener('click', function(e) {
            if (!confirm('确定要删除吗？这个操作无法撤销。')) {
                e.preventDefault();
            }
        });
    });
});

// 点赞动画
function animateLike(button) {
    button.classList.add('liked');
    setTimeout(function() {
        button.classList.remove('liked');
    }, 1000);
}

// 回到顶部按钮
function scrollToTop() {
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// 检测滚动显示回到顶部按钮
window.addEventListener('scroll', function() {
    var scrollTopButton = document.getElementById('scrollTopButton');
    if (scrollTopButton) {
        if (window.pageYOffset > 300) {
            scrollTopButton.style.display = 'block';
        } else {
            scrollTopButton.style.display = 'none';
        }
    }
});