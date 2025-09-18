'use client';

import React, { useEffect, useState } from 'react';
import { X, CheckCircle, AlertCircle, Info, AlertTriangle } from 'lucide-react';
import styles from './toast.module.scss';

export type ToastType = 'success' | 'error' | 'info' | 'warning';

export interface ToastProps {
  id: string;
  type: ToastType;
  title: string;
  message?: string;
  duration?: number;
  onClose: (id: string) => void;
}

const Toast: React.FC<ToastProps> = ({
  id,
  type,
  title,
  message,
  duration = 5000,
  onClose,
}) => {
  const [isVisible, setIsVisible] = useState(false);
  const [isRemoving, setIsRemoving] = useState(false);

  useEffect(() => {
    // Trigger entrance animation
    const timer = setTimeout(() => setIsVisible(true), 10);
    return () => clearTimeout(timer);
  }, []);

  useEffect(() => {
    if (duration > 0) {
      const timer = setTimeout(() => {
        handleClose();
      }, duration);
      return () => clearTimeout(timer);
    }
  }, [duration]);

  const handleClose = () => {
    setIsRemoving(true);
    setTimeout(() => {
      onClose(id);
    }, 500);
  };

  const getIcon = () => {
    switch (type) {
      case 'success':
        return <CheckCircle className={styles.icon} />;
      case 'error':
        return <AlertCircle className={styles.icon} />;
      case 'warning':
        return <AlertTriangle className={styles.icon} />;
      case 'info':
        return <Info className={styles.icon} />;
      default:
        return <Info className={styles.icon} />;
    }
  };

  return (
    <div
      className={`${styles.toast} ${styles[type]} ${
        isVisible && !isRemoving ? styles.show : ''
      } ${isRemoving ? styles.hide : ''}`}
      role="alert"
      aria-live="polite"
    >
      <div className={styles.content}>
        <div className={styles.iconWrapper}>
          {getIcon()}
        </div>
        <div className={styles.textContent}>
          <h4 className={styles.title}>{title}</h4>
          {message && <p className={styles.message}>{message}</p>}
        </div>
        <button
          className={styles.closeButton}
          onClick={handleClose}
          aria-label="Close notification"
        >
          <X size={16} />
        </button>
      </div>
      <div className={styles.progressBar}>
        <div
          className={styles.progressFill}
          style={{ animationDuration: `${duration}ms` }}
        />
      </div>
    </div>
  );
};

export default Toast;