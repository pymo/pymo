// pymo_pack.h : main header file for the PYMO_PACK application
//

#if !defined(AFX_PYMO_PACK_H__F158C6BB_5CA7_4CD1_8A59_0A9DC2F2566E__INCLUDED_)
#define AFX_PYMO_PACK_H__F158C6BB_5CA7_4CD1_8A59_0A9DC2F2566E__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"		// main symbols

/////////////////////////////////////////////////////////////////////////////
// CPymo_packApp:
// See pymo_pack.cpp for the implementation of this class
//

class CPymo_packApp : public CWinApp
{
public:
	CPymo_packApp();

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CPymo_packApp)
	public:
	virtual BOOL InitInstance();
	//}}AFX_VIRTUAL

// Implementation

	//{{AFX_MSG(CPymo_packApp)
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_PYMO_PACK_H__F158C6BB_5CA7_4CD1_8A59_0A9DC2F2566E__INCLUDED_)
