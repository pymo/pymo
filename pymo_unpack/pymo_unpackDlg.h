// pymo_unpackDlg.h : header file
//

#if !defined(AFX_PYMO_UNPACKDLG_H__579D5AB3_64A7_45F8_A868_727A0E8F1833__INCLUDED_)
#define AFX_PYMO_UNPACKDLG_H__579D5AB3_64A7_45F8_A868_727A0E8F1833__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

/////////////////////////////////////////////////////////////////////////////
// CPymo_unpackDlg dialog

class CPymo_unpackDlg : public CDialog
{
// Construction
public:
	CPymo_unpackDlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	//{{AFX_DATA(CPymo_unpackDlg)
	enum { IDD = IDD_PYMO_UNPACK_DIALOG };
	CString	m_sRtDataFilePath;
	CString	m_strExtension;
	CString	m_strPath;
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CPymo_unpackDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	//{{AFX_MSG(CPymo_unpackDlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	afx_msg void OnButton1();
	afx_msg void OnButton3();
	virtual void OnOK();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_PYMO_UNPACKDLG_H__579D5AB3_64A7_45F8_A868_727A0E8F1833__INCLUDED_)
