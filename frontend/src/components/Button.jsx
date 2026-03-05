import './Button.css';

function Button({ 
  children, 
  variant = 'primary', 
  size = 'medium',
  type = 'button',
  disabled = false,
  onClick,
  className = '',
  ...props 
}) {
  return (
    <button
      type={type}
      className={`btn btn-${variant} btn-${size} ${className}`}
      disabled={disabled}
      onClick={onClick}
      {...props}
    >
      {children}
    </button>
  );
}

export default Button;
