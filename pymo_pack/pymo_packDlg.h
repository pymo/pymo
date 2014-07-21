// pymo_packDlg.h : header file
//

#if !defined(AFX_PYMO_PACKDLG_H__3120F50C_9FAB_4E83_8A27_FA3D839984D8__INCLUDED_)
#define AFX_PYMO_PACKDLG_H__3120F50C_9FAB_4E83_8A27_FA3D839984D8__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

/////////////////////////////////////////////////////////////////////////////
// CPymo_packDlg dialog

class CPymo_packDlg : public CDialog
{
// Construction
public:
	CPymo_packDlg(CWnd* pParent = NULL);	// standard constructor

// Dialog Data
	//{{AFX_DATA(CPymo_packDlg)
	enum { IDD = IDD_PYMO_PACK_DIALOG };
	CString	m_strPath;
	CString	m_sRtDataFilePath;
	//}}AFX_DATA

	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CPymo_packDlg)
	protected:
	virtual void DoDataExchange(CDataExchange* pDX);	// DDX/DDV support
	//}}AFX_VIRTUAL

// Implementation
protected:
	HICON m_hIcon;

	// Generated message map functions
	//{{AFX_MSG(CPymo_packDlg)
	virtual BOOL OnInitDialog();
	afx_msg void OnSysCommand(UINT nID, LPARAM lParam);
	afx_msg void OnPaint();
	afx_msg HCURSOR OnQueryDragIcon();
	afx_msg void OnButton1();
	afx_msg void OnButton2();
	virtual void OnOK();
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_PYMO_PACKDLG_H__3120F50C_9FAB_4E83_8A27_FA3D839984D8__INCLUDED_)
